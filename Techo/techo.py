import json
from flask import Flask, render_template, request, Response
from database import Database


app = Flask(__name__)


def get_db():
    return Database("localhost", 27017, "techo")


@app.route("/")
def home():
    return "WIP"


@app.route("/add-tech", methods=['GET'])
def add_tech():
    return render_template('add-tech.html')


@app.route("/techs", methods=['GET'])
def get_techs():
    records = get_db().retrieve_all('techs')
    return json.dumps(records)


@app.route("/techs", methods=['POST'])
def techs():
    name_of_tech = request.form['tech']
    db = get_db()
    id_of_record = db.save("techs", {'name': name_of_tech})
    return Response(
        "thanks %s created, id: %s" % (name_of_tech, id_of_record),
        status=201,
        headers={'Location': '/techs/%s' % id_of_record}
    )


@app.route("/techs/<tech_id>", methods=['GET'])
def get_tech(tech_id):
    record = get_db().retrieve('techs', tech_id)
    return json.dumps(record)


@app.route("/compare/<tech1>/<tech2>")
def compare(tech1, tech2):
    db = get_db()
    record1 = get_db().retrieve('techs', tech1)
    record2 = get_db().retrieve('techs', tech2)
    return render_template('compare.html', tech1=record1, tech2=record2)


@app.route("/ratings", methods=['POST'])
def rating():
    return request.form['which-tech']

if __name__ == "__main__":
    app.debug = True
    app.run()
