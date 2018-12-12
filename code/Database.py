#!/usr/bin/python3

import mysql.connector
from mysql.connector import connection
from mysql.connector import errorcode


class Database:

    def __init__(self, config):
        try:
            self.conn = mysql.connector.connect(**config)
        
        except mysql.connector.Error as err:

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Username or password wrong")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Schema does not exist")
            else:
                print(err)

    def __del__(self):
        self.conn.close()

    def query(self, query):
        
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor


class DatabaseKDD(Database):

    user        =   'estudiante'
    password    =   'contraseña1'
    host        =   'plazaromero.ddns.net'
    squema      =   'kddcup2015'

    def __init__(self):
        
        config      =   {
            'user'      :   self.user,
            'password'  :   self.password,
            'host'      :   self.host,
            'database'  :   self.squema,
            'raise_on_warnings': True
        }
        
        super().__init__(config)


if __name__ == '__main__':

    db      = DatabaseKDD()
    data    = db.query("SELECT course_id, module_id FROM objets")

    for (course_id, module_id) in data:
        print(course_id, module_id)

    
