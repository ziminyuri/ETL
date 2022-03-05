from elasticsearch import Elasticsearch, helpers
import backoff
import json


class Loader:
    def __init__(self, es):
        self.es = Elasticsearch([f'http://{es.host}:{es.port}'])

    @backoff.on_exception(backoff.expo, BaseException)
    def load(self, data):

        try:
            for d in data:
                # helpers.bulk(self.es, d.dict(), index="movies")
                # self.es.index(
                #     index='movies',
                #     doc_type="doc",
                #     # id=data.id,
                #     body=d.dict(),
                # )
                self.es.index(
                    index='movies',
                    # doc_type='doc',
                    id=d.id,
                    body=json.dumps(d.dict())
                )

        except Exception as e:
            print(e)
