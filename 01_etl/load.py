import json

import backoff
from elasticsearch import Elasticsearch


class Loader:

    @backoff.on_exception(backoff.expo, BaseException)
    def __init__(self, es):
        self.es = Elasticsearch([f'http://{es.host}:{es.port}'])

    @backoff.on_exception(backoff.expo, BaseException)
    def load(self, data):
        for d in data:
            self.es.index(
                index='movies',
                id=d.id,
                body=json.dumps(d.dict())
            )
