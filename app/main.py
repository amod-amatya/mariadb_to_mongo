from flask import Flask, redirect, url_for, render_template, request
import logging, mariadb, sys, pymongo, configparser, os
from app.db_connect import DbConnect
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

root_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(root_dir, "conf/database_config.ini")
config = configparser.ConfigParser()
config.read(config_file)

#Mongodb
cluster = MongoClient(config['mongodb']['host'])
mongodb = cluster[config['mongodb']['database']]
collection =  mongodb[config['mongodb']['collection']]
# list = [a , b ,c, d]
# collection.insertMany( [
# { _id: "MongoDB", ancestors: [ "Books", "Programming", "Databases" ], parent: "Databases" },
# { _id: "dbm", ancestors: [ "Books", "Programming", "Databases" ], parent: "Databases" },
# ])
#DB connection constructor initialize
db_connect = DbConnect(app, config, mongodb, collection)

##Connect to mariadb server
cur = db_connect.mariadb_connect()  

## Connection for mongodb 
mongodb_connect_list = db_connect.mongodb_connect(cur)


@app.route("/", methods=["POST", "GET"])
def home_view():
        if request.method == "POST":
                if request.form["button"] == "Start":
                        data = request.form["usecase"]
                        app.logger.debug('Data ' + data)
                        mongodb_connect_list.insert(0,data)
                elif request.form["button"] == "Get-Data":
                        insert_document_mongodb(mongodb_connect_list)
                        app.logger.debug('Updating UI with %s', mongodb_connect_list)
                        return render_template("index.html", list_components=mongodb_connect_list)

        return render_template("index.html")

@app.route("/db")
def db_view():

        return "<h1>DB section</h1>"

def insert_document_mongodb(list_components):
        """ Insert rows of Component_View table from mariadb server to mongodb """

        dict_components = {}
        dict_components["components"] = list_components
        dict_components["time_stamp"] = str(datetime.now())
        app.logger.debug('Dictionary components %s',dict_components)

        collection.insert_one(dict_components)

@app.route("/move_forward")
def move_forward():
    #Moving forward code
    return (''), 204

# if __name__ == '__main__':
#    app.run(debug=True)

