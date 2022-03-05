from state import JsonFileStorage, State
from psycopg2.extras import RealDictCursor
from config import PostgresConfig, ElasticConfig
from etl_process import ETLProcess




# def get_data(pg_conn, column, table):
#     sql = f"""
#     SELECT
#         fw.id,
#         fw.title,
#         fw.type,
#         fw.description,
#         fw.rating as imdb_rating,
#         fw.created_at,
#         fw.updated_at,
#     JSON_AGG(DISTINCT jsonb_build_object('id', g.id, 'name', g.name)) AS genre
#     ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'actor') AS actors_names,
#     ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'writer') AS writers_names,
#     GREATEST(
#         fw.updated_at,
#         MAX(g.updated_at),
#         MAX(DISTINCT p.updated_at) FILTER (WHERE pfw.role = 'writer'),
#         MAX(DISTINCT p.updated_at) FILTER (WHERE pfw.role = 'actor'),
#         MAX(DISTINCT p.updated_at) FILTER (WHERE pfw.role = 'director')
#     ) as all_updated_at,
#     JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'director') -> 0 AS director,
#     JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'actor') AS actors,
#     JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'writer') AS writers
#     FROM content.film_work fw
#     LEFT OUTER JOIN content.genre_film_work gfw ON fw.id = gfw.filmwork_id
#     LEFT OUTER JOIN content.genre g ON (gfw.genre_id = g.id)
#     LEFT OUTER JOIN content.person_film_work pfw ON (fw.id = pfw.filmwork_id)
#     LEFT OUTER JOIN content.person p ON (pfw.person_id = p.id)
#     GROUP BY fw.id, fw.title, fw.description, fw.rating
#     ORDER BY fw.updated_at
#     """
#
#     cursor = pg_conn.cursor(cursor_factory=RealDictCursor)
#     cursor.execute(sql)
#     return cursor.fetchmany(BATCH)


if __name__ == '__main__':
    db = PostgresConfig()
    es = ElasticConfig()
    json_file_storage = JsonFileStorage('state.json')
    state = State(json_file_storage)

    etl = ETLProcess(db, es, state)
    etl.process()
    # es = Elasticsearch([os.getenv('ES_HOST', 'http://localhost:9200/')])


