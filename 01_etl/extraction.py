from config import BATCH
from psycopg2.extras import DictCursor


class Extraction:
    def __init__(self, conn):
        self.cursor = conn.cursor(cursor_factory=DictCursor)

    def extracting(self, state_updated_at):
        self.cursor.execute(
            f"""
            SELECT
                fw.id,
                fw.title,
                fw.description,
                fw.rating as imdb_rating,
                fw.updated_at,
            ARRAY_AGG(DISTINCT g.name) AS genre,
            ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'actor') AS actors_names,
            ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'writer') AS writers_names,
            GREATEST(
                fw.updated_at,
                MAX(g.updated_at),
                MAX(DISTINCT p.updated_at) FILTER (WHERE pfw.role = 'writer'),
                MAX(DISTINCT p.updated_at) FILTER (WHERE pfw.role = 'actor'),
                MAX(DISTINCT p.updated_at) FILTER (WHERE pfw.role = 'director')
            ) as all_updated_at,
            ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'director') AS director,
            JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'actor') AS actors,
            JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'writer') AS writers
            FROM content.film_work fw
            LEFT OUTER JOIN content.genre_film_work gfw ON fw.id = gfw.filmwork_id
            LEFT OUTER JOIN content.genre g ON (gfw.genre_id = g.id)
            LEFT OUTER JOIN content.person_film_work pfw ON (fw.id = pfw.filmwork_id)
            LEFT OUTER JOIN content.person p ON (pfw.person_id = p.id)
            GROUP BY fw.id, fw.title, fw.description, fw.rating
            HAVING fw.updated_at >= '{state_updated_at}' OR MAX(g.updated_at) >= '{state_updated_at}' OR MAX(p.updated_at) >= '{state_updated_at}'
            ORDER BY all_updated_at
        """
        )

        return self.cursor.fetchmany(BATCH)



