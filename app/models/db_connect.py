import collections
import logging
from typing import Collection
import mariadb
import sys
import configparser
import pymongo
import os
from datetime import datetime
from pymongo import MongoClient

class DbConnect:
    automobile_collection = ''
    def __init__(self, app, config):
        self.app = app
        self.config = config

    def mongodb_connect(self):
        """ Mongodb connection setup """

        cluster = MongoClient(self.config['mongodb']['host'])
        mongodb = cluster[self.config['mongodb']['database']]
        self.automobile_collection = mongodb[self.config['mongodb']['automobile_collection']]
        self.component_collection = mongodb[self.config['mongodb']['component_collection']]
        self.app.logger.debug('Connected to to MongoDB Platform')
        return self.component_collection

    def mariadb_connect(self):
        """ Connection for mariadb server """

        try:
            conn = mariadb.connect(
                user=self.config['mariadb']['user'],
                password=self.config['mariadb']['password'],
                host=self.config['mariadb']['host'],
                port=self.config.getint('mariadb', 'port'),
                database=self.config['mariadb']['database'],
                ssl=True)
            self.app.logger.debug('Connected to to MariaDB Platform')

        except mariadb.Error as e:
            self.app.logger.error('Error connecting to MariaDB Platform')

        return conn.cursor()

    def get_list_from_mariadb(self, cur):
        """ Connection for mongodb atlas """
        try:
            self.cur = cur
            list_components = []
            self.app.logger.debug('Getting Component data')

            # Get 5 rows from Component_View table in mariadb server
            self.cur.execute("SELECT * FROM Component_View LIMIT 5")
            for a, b in self.cur:
                list_components.append(b)

            self.app.logger.debug('List of components %s', list_components)
            return list_components
        except:
            self.app.logger.error('Error connecting to Mongodb Platform')

    def insert_document_mongodb(self, list_components):
        """ Insert rows of Component_View table from mariadb server to mongodb """

        dict_components = {}
        dict_components["components"] = list_components
        dict_components["time_stamp"] = str(datetime.now())
        self.app.logger.debug('Dictionary components %s', dict_components)
        self.automobile_collection.insert_one(dict_components)
