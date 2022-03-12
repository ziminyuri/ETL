from config import ElasticConfig, PostgresConfig
from etl_process import ETLProcess
from state import JsonFileStorage, State

if __name__ == '__main__':
    db: PostgresConfig = PostgresConfig()
    es: ElasticConfig = ElasticConfig()
    json_file_storage: JsonFileStorage = JsonFileStorage('state.json')
    state: State = State(json_file_storage)

    etl: ETLProcess = ETLProcess(db, es, state)
    etl.process()


