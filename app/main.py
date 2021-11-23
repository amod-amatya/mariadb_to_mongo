from flask import Flask, redirect, url_for, render_template, request
import logging, mariadb, sys, pymongo, configparser, os
from app.mariadb_connect import MariadbConnect
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
root_dir = os.path.dirname(os.path.abspath(__file__))
print ("qweqwe " + root_dir)
config_file = os.path.join(root_dir, "conf/database_config.ini")
print ("asdads " + config_file)
config = configparser.ConfigParser()
config.read(config_file)
db_connect = MariadbConnect(app, config)
cur = db_connect.mariadb_connect()

## Connection for mongodb 
cluster = MongoClient(config['mongodb']['host'])
db = cluster[config['mongodb']['database']]
collection =  db[config['mongodb']['collection']]

# post = {"_id": 0, "name": "amod", "score": 5}
# collection.insert_one(post)

@app.route("/")
def home_view():
        return render_template("index.html")

@app.route("/get_data", methods=['POST'])
def get_data():
        list_components = []
        app.logger.debug('Getting Component data')

        # Get 5 rows from Component_View table in mariadb server
        cur.execute("SELECT * FROM Component_View LIMIT 5") 
        for a, b  in cur: 
                app.logger.debug('Component data is %s and %s', a, b)
                list_components.append(b)
        
        app.logger.debug('List of components %s',list_components)

        insert_document_mongodb(list_components)

        # Upate UI with list of components 
        if request.method == 'POST':
                if request.form['getdata'] == 'getdata':
                        app.logger.debug('Updating UI with %s', list_components)  
                        return render_template("index.html", list_components=list_components)
                else:
                        return render_template("index.html")
        
@app.route("/db")
def db_view():
        return "<h1>DB section</h1>"

def insert_document_mongodb(list_components):
        """ Insert rows of Component_View table from mariadb server to mongodb """

        dict_components = {}
        dict_components["components"] = list_components
        dict_components["time_stamp"] = datetime.now()
        app.logger.debug('Dictionary components %s',dict_components)         
        collection.insert_one(dict_components)

# if __name__ == '__main__':
#    app.run(debug=True)

