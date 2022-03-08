import psycopg2
from config import LOGGER
from extraction import Extraction
from datetime import datetime
from transform import transformation
from load import Loader
import backoff
import time


class ETLProcess:
    def __init__(self, db, es, state):
        self.db = db
        self.es = es
        self.state = state
        self.timeout = 10

        if not self.state.get_state('updated_at'):
            self.state.set_state('updated_at', datetime(year=1900, month=1, day=1).strftime("%Y-%m-%d %H:%M:%S.%f"))

    def process(self):
        while True:
            try:
                LOGGER.info('Start upload batch from PG to Elastic')
                conn = self.get_db_connection()
                data = Extraction(conn).extracting(self.state.get_state('updated_at'))
                new_updated_at = self.get_new_state(data[-1])
                if new_updated_at > datetime.strptime(self.state.get_state('updated_at'), "%Y-%m-%d %H:%M:%S.%f"):
                    data = transformation(data)
                    Loader(self.es).load(data)
                    self.state.set_state('updated_at', new_updated_at.strftime("%Y-%m-%d %H:%M:%S.%f"))
                    LOGGER.info('Successfull upload batch from PG to Elastic')
                    self.timeout = 10

                else:
                    LOGGER.info('No new batch to upload from PG to Elastic')
                    self.timeout += self.timeout

            except Exception as e:
                LOGGER.exception(f'{e}')

            time.sleep(self.timeout)

    @backoff.on_exception(backoff.expo, BaseException)
    def get_db_connection(self):
        LOGGER.info(f'Connect to database')
        conn = psycopg2.connect(**self.db.dict())
        return conn

    @staticmethod
    def get_new_state(row):
        return dict(row).get('all_updated_at')
