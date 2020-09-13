import flask
from flask import request, jsonify
import sqlite3
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>API CVE</h1>
<p>Um prototipo de API para consultar CVE do 'cve.mitre.org'</p>'''


@app.route('/api/v1/resources/cve/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('cve.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_cve = cur.execute('SELECT * FROM tripdata;').fetchall()

    return jsonify(all_cve)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>Roi, desculpa, mas... não achei a pagina...</p>", 404


@app.route('/api/v1/resources/cve', methods=['GET'])
def api_filter():
    query_parameters = request.args

    nome = query_parameters.get('nome')
    descricao = query_parameters.get('descricao')

    query = "SELECT * FROM tripdata WHERE"
    to_filter = []

    if nome:
        query += ' nome=? like'
        to_filter.append(nome)
    if descricao:
        query += ' descricao=?'
        to_filter.append(descricao)

    if not (nome or descricao):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('cve.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

app.run()

#http://127.0.0.1:5000/api/v1/resources/cve?nome=CVE-1999-0001