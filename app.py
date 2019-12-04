# app.py
import sqlite3
import service
#import request
from flask import request
from flask import jsonify
from flask import Flask           # import flask
app = Flask(__name__)             # create an app instance

@app.route("/")                   # at the end point /
def hello():                      # call method hello
    return "Hello World!"   
          # which returns "hello world"

@app.route("/<name>")              # at the end point /<name>
def hello_name(name):              # call method hello_name
    return "Hello "+ name  


@app.route("/color", methods =["POST"])
def create_color():
    return service.ColorsService().create(jsonify(request.json))




class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('colors.db')
        self.create_person_table()
        self.create_colors_table()
        # Why are we calling user table before to_do table
        # what happens if we swap them?

    def create_colors_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS "Colors" (
          id INTEGER PRIMARY KEY,
          Color TEXT,
          
          UserId INTEGER FOREIGNKEY REFERENCES User(_id)
        );
        """

        self.conn.execute(query)
    def create_person_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Person" (
          id INTEGER PRIMARY KEY,
          Name TEXT,
          
          UserId INTEGER FOREIGNKEY REFERENCES Person(_id)
        );
        """




if __name__ == "__main__":
	Schema()        # on running python app.py
	app.run(debug = True) 