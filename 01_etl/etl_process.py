import psycopg2
from config import LOGGER
from extraction import Extraction
from datetime import datetime
from transform import transformation
from load import Loader
import backoff


class ETLProcess:
    def __init__(self, db, es, state):
        self.db = db
        self.es = es
        self.state = state

        if not self.state.get_state('updated_at'):
            self.state.set_state('updated_at', datetime(year=1900, month=1, day=1).strftime("%Y-%m-%d %H:%M:%S"))

    def process(self):
        conn = self.get_db_connection()
        data = Extraction(conn).extracting(self.state.get_state('updated_at'))
        data = transformation(data)
        Loader(self.es).load(data)

    @backoff.on_exception(backoff.expo, BaseException)
    def get_db_connection(self):
        LOGGER.info(f'Connect to database')
        conn = psycopg2.connect(**self.db.dict())
        return conn
