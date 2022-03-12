import time
from datetime import datetime

import backoff
import psycopg2
from psycopg2.extensions import connection
from config import LOGGER, PostgresConfig, ElasticConfig
from extraction import Extraction
from load import Loader
from transform import transformation
from state import State
from psycopg2.extras import DictRow


class ETLProcess:
    def __init__(self, db: PostgresConfig, es: ElasticConfig, state: State) -> None:
        self.db: PostgresConfig = db
        self.es: ElasticConfig = es
        self.state: State = state
        self.timeout: int = 10

        if not self.state.get_state('updated_at'):
            self.state.set_state('updated_at', datetime.min.strftime("%Y-%m-%d %H:%M:%S.%f"))

    def process(self) -> None:
        while True:
            try:
                LOGGER.info('Start upload batch from PG to Elastic')
                conn: connection = self.get_db_connection()
                data: list = Extraction(conn).extracting(self.state.get_state('updated_at'))
                new_updated_at: datetime = self.get_new_state(data[-1])

                if new_updated_at > datetime.strptime(self.state.get_state('updated_at'), "%Y-%m-%d %H:%M:%S.%f"):
                    data: list = transformation(data)
                    Loader(self.es).load(data)
                    self.state.set_state('updated_at', new_updated_at.strftime("%Y-%m-%d %H:%M:%S.%f"))
                    LOGGER.info('Successfull upload batch from PG to Elastic')
                    self.timeout: int = 10

                else:
                    LOGGER.info('No new batch to upload from PG to Elastic')
                    self.timeout += self.timeout

            except Exception as e:
                LOGGER.exception(f'{e}')

            time.sleep(self.timeout)

    @backoff.on_exception(backoff.expo, BaseException)
    def get_db_connection(self) -> connection:
        print(self.db.dict())
        LOGGER.info(f'Connect to database')
        return psycopg2.connect(**self.db.dict())

    @staticmethod
    def get_new_state(row: DictRow) -> datetime:
        return dict(row).get('all_updated_at')
