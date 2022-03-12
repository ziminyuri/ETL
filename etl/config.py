import logging

from pydantic import BaseSettings, Field

file_log = logging.FileHandler('app.log')
console_out = logging.StreamHandler()

logging.basicConfig(
    handlers=(file_log, console_out),
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

LOGGER = logging.getLogger()

BATCH = 100


class PostgresConfig(BaseSettings):
    """ Конфиги подключения к PG """

    dbname: str = Field(..., env='POSTGRES_DB')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    host: str = Field(..., env='POSTGRES_HOST')
    port: str = Field(..., env='POSTGRES_PORT')

    # class Config:
    #     env_file: str = '../.env'


class ElasticConfig(BaseSettings):
    host: str = Field(..., env='ES_HOST')
    port: str = Field(..., env='ES_PORT')

    # class Config:
    #     env_file: str = '../.env'
