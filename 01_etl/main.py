from config import ElasticConfig, PostgresConfig
from etl_process import ETLProcess
from state import JsonFileStorage, State

if __name__ == '__main__':
    db = PostgresConfig()
    es = ElasticConfig()
    json_file_storage = JsonFileStorage('state.json')
    state = State(json_file_storage)

    etl = ETLProcess(db, es, state)
    etl.process()


