import logging, mariadb, sys, configparser
import pymongo, os

class DbConnect:
    def __init__(self, app, config, mongodb, collection):
        self.app = app
        self.config = config
        self.momgodb = mongodb
        self.collection = collection

    def mariadb_connect(self):
        """ Connection for mariadb server """

        try: conn = mariadb.connect( 
                user=self.config['mariadb']['user'], 
                password=self.config['mariadb']['password'], 
                host=self.config['mariadb']['host'], 
                port=self.config.getint('mariadb', 'port'), 
                database=self.config['mariadb']['database'],
                ssl=True)
        except mariadb.Error as e: 
                self.app.logger.error('Error connecting to MariaDB Platform')

        return conn.cursor()
    
    def mongodb_connect(self, cur):
         """ Connection for mongodb atlas """
         try:
            self.cur = cur
            list_components = []
            self.app.logger.debug('Getting Component data')

            # Get 5 rows from Component_View table in mariadb server
            self.cur.execute("SELECT * FROM Component_View LIMIT 5") 
            for a, b  in self.cur:
                self.app.logger.debug('Component data is %s and %s', a, b)
                list_components.append(b)
            
            self.app.logger.debug('List of components %s', list_components)
            return list_components
         except:
            self.app.logger.error('Error connecting to Mongodb Platform')