from flask import Flask, jsonify, abort, request
from tamilmv import Tamilmv
from utils import imdb_retriver
import os

app = Flask(__name__)

# Streaks_Movies Manifest
MANIFEST = {
    'id': 'org.stremio.Streaks_Movies',
    'version': '1.0.0',

    'name': 'Streaks Movies',
    'description': 'Add-on for Streaming Indian Regional Movies. As of version_1 only one Domain is supported',

    'types': ['movie'],

    'catalogs': [],

    'resources': [
        {'name': 'stream', 'types': [
            'movie'], 'idPrefixes': ['tt', 'hpy']}
    ]
}


# Intial for STREAMS dictionary Later would be populated by search results
STREAMS = {}

# Helper function for JSON response
def respond_with(data):
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp

@app.route('/manifest.json')
def addon_manifest():
    return respond_with(MANIFEST)

@app.route('/stream/<type>/<id>.json')
def addon_stream(type, id):
    if type not in MANIFEST['types']:
        abort(404)

    title=imdb_retriver.fetch_movie_title(id)
    STREAMS=Tamilmv.tamilmv(title,id)
    streams = {'streams': []}
    if type in STREAMS and id in STREAMS[type]:
        streams['streams'] = STREAMS[type][id]
    return respond_with(streams)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))  
    app.run(debug=True, port=port, host='0.0.0.0')