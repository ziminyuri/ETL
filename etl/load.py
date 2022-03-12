import json

import backoff
from elasticsearch import Elasticsearch, helpers
import subprocess


class Loader:

    @backoff.on_exception(backoff.expo, BaseException)
    def __init__(self, es):
        self.es = Elasticsearch([f'http://{es.host}:{es.port}'])

        if not self.es.indices.exists(index='movies'):
            subprocess.call(['sh', './indexes/create_index.sh'])

    @staticmethod
    def gen_data(data):
        for d in data:
            yield {
                "_index": "movies",
                "body": json.dumps(d.dict()),
            }

    @backoff.on_exception(backoff.expo, BaseException)
    def load(self, data):
        try:
            new_data = [
                {"_index": "movies", "_id": d.id, "_source": d.json()}
                for d in data
            ]
            helpers.bulk(self.es, new_data)
        except Exception as e:
            print(e)
        # for d in data:
        #     self.es.index(
        #         index='movies',
        #         id=d.id,
        #         body=json.dumps(d.dict())
        #     )
