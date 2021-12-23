from flask import Flask, redirect, url_for, render_template, request, session
from flask_session import Session
import logging, mariadb, sys, pymongo, configparser, os
from app.models.db_connect import DbConnect
from app.models.models import *
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

root_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(root_dir, "conf/database_config.ini")
config = configparser.ConfigParser()
config.read(config_file)

#DB connection constructor initialize
db_connect = DbConnect(app, config)

##Connect to mongodb server
component_collection = db_connect.mongodb_connect()

##Connect to mariadb server
cur = db_connect.mariadb_connect()

## Get component list from mariadb
component_list = db_connect.get_list_from_mariadb(cur)

add_components(component_collection)

@app.route("/", methods=["POST", "GET"])
def home_view():
        interfaces = ['Remote','Bluetooth','Sensor','Wi-fi','Cellular','OBD','V2X']
        session['selected_interface']  = request.form.get('interfaces')

        if request.method == "POST":
                if request.form["button"] == "Start":
                        data = request.form["usecase"]
                        # app.logger.debug('Data ' + selected_interface)
                        component_list.insert(0,data)
                        return redirect(url_for('db_view'))

                elif request.form["button"] == "get-data":
                        db_connect.insert_document_mongodb(component_list)
                        app.logger.debug('Updating UI with %s', component_list)
                        return render_template("index.html", list_components=component_list)

        return render_template("index.html", interfaces=interfaces)

@app.route("/db", methods=['GET', 'POST'])
def db_view():

        selected_interface = session.get('selected_interface', None)
        app.logger.debug('Data ' + selected_interface)
        keyword_extracted = "traffic"
        # if keyword_extracted.casefold() == "Traffic":


        if selected_interface == "Sensor":
                input_components_dropdown = input_components
        elif selected_interface == "OBD":
                input_components_dropdown = ['Diagnostic Port']
        elif selected_interface == "Bluetooth":
                input_components_dropdown = [network_input_components[1]]
        elif selected_interface == "Wi-fi":
                input_components_dropdown = [network_input_components[2]]
        elif selected_interface == "Cellular":
                input_components_dropdown = [network_input_components[3]]
        elif selected_interface == "V2X":
                input_components_dropdown = network_input_components[-1:]
        elif selected_interface == "Remote":
                input_components_dropdown = network_input_components
        else:
                input_components_dropdown = input_components
        
        mid_components = ['DASy', 'CGU']
        return render_template("component.html", environment1=environment1, environment2=environment2, input_components=input_components_dropdown,
                                         mid_components = mid_components, output_components=output_components, 
                                         output_components_VCU=output_components_VCU)


