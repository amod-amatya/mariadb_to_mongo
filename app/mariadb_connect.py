import logging, mariadb, sys, configparser

class MariadbConnect:
    def __init__(self, app, config):
        self.app = app
        self.config = config

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