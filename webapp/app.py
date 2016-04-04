from flask import Flask, render_template, request
from elasticsearch import Elasticsearch, exceptions

app = Flask(__name__)
es = Elasticsearch()

keywords = ['movies','sports','music','finance','technology','fashion','science','travel','health','cricket','india']

@app.route('/')
def index():
    query = request.args.get('q', '')
    res = es.search(
        index="faaltu",
        body={
            "query": {"match": {"text": query}},
            "size": 750 # max document size
        })
    coords, results = [], []
    if res["hits"]["hits"]:
        coords = [r["_source"]["coordinates"] for r in res["hits"]["hits"]]
        results = [r["_source"]["text"] for r in res["hits"]["hits"]]
    return render_template("index.html",
                           coords=coords,
                           keywords=keywords,
                           query=query,
                           results=results)

if __name__ == "__main__":
    app.run(debug=True)
