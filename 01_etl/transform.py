from models import Film


def transformation(data):
    new_data = []
    for row in data:
        f = Film(
            id=dict(row).get('id'),
            title=dict(row).get('title'),
            imdb_rating=dict(row).get('imdb_rating'),
            # genre=dict(row).get('genre'),
            genre='adventure',
            description=dict(row).get('description'),
            director=dict(row).get('director'),
            actors_names=_change_None_to_list(dict(row).get('actors_names')),
            writers_names=_change_None_to_list(dict(row).get('writers_names')),
            actors=_change_None_to_list(dict(row).get('actors')),
            writers=_change_None_to_list(dict(row).get('writers')),
        )
        new_data.append(f)

    return new_data


def _change_None_to_list(value):
    if value is None:
        return []
    else:
        return value



