from models import Film


def transformation(data: list) -> list:
    new_data: list = []

    for row in data:
        row: dict = dict(row)
        f: Film = Film(
            id=row.get('id'),
            title='' if row.get('title') is None else row.get('title'),
            imdb_rating='' if row.get('imdb_rating') is None else row.get('imdb_rating'),
            genre=[] if row.get('genre') is None else row.get('genre'),
            description='' if row.get('description') is None else row.get('description'),
            director=[] if row.get('director') is None else row.get('director'),
            actors_names=[] if row.get('actors_names') is None else row.get('actors_names'),
            writers_names=[] if row.get('writers_names') is None else row.get('writers_names'),
            actors=row.get('actors'),
            writers=row.get('writers'),
        )
        new_data.append(f)

    return new_data








