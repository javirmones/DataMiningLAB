#!/usr/bin/python3
# -*- coding: utf-8 -*-

import mysql.connector
import pandas as pd
import numpy
from mysql.connector import connection
from mysql.connector import errorcode

user                            =   'estudiante'
password                        =   'contraseña1'
host                            =   'plazaromero.ddns.net'
squema                          =   'kddcup2015'
ruta_cursos_iteracciones_modulo =   'data/cursos_modulo.csv'

config      =   {
    'user'      :   user,
    'password'  :   password,
    'host'      :   host,
    'database'  :   squema,
    'raise_on_warnings': True
}

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

    def __init__(self):
        global config
        super().__init__(config)

def to_csv(path,dataframe):
    dataframe.to_csv(path)

def make_querys():

    pass

if __name__ == '__main__':

    lista_id_curso = []
    lista_curso = []
    lista_usuario = []
    lista_interaccion = []

    db        =  DatabaseKDD()
    data      =  db.query("SELECT course_id FROM objets")

    for course_id in data:
        lista_id_curso.append(list(course_id))

    data_curso      =  db.query("SELECT module_id FROM objets")
    for module_id in data_curso:
        lista_curso.append(list(module_id))
        
    data_user = db.query("SELECT username FROM enrollment_train")

    for username in data_user:
        lista_usuario.append(list(username))
    

    data_interaccion = db.query("SELECT COUNT(t1.enrollment_id)"
    +" FROM enrollment_train AS t1"
        +" JOIN log_train AS t2 on t1.enrollment_id = t2.enrollment_id"
    +" GROUP BY t1.username")

    for enrollment_id in data_interaccion:
        lista_interaccion.append(list(enrollment_id))


    df = pd.DataFrame(lista_id_curso,columns = ['id_curso'])
    df_cursos = pd.DataFrame(lista_curso, columns = ['curso'])
    df_usuarios = pd.DataFrame(lista_usuario, columns =['usuarios'])
    df_int = pd.DataFrame(lista_interaccion, columns=['interacciones_curso'])

    df_1 = pd.concat([df, df_usuarios], axis=1, join_axes=[df.index])
    df_2 = pd.concat([df_1, df_cursos], axis=1, join_axes=[df_1.index])
    df_3 = pd.concat([df_2, df_int], axis=1, join_axes=[df_2.index])
    

    to_csv(ruta_cursos_iteracciones_modulo,df_3)

    