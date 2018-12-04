#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy

ruta_cursos_iteracciones_modulo =   'data/cursos_modulo.csv'
ruta_cursos_iteracciones_modulo_preprocesado = 'data/cursos_modulo_preprocesado.csv'

def read_dataset(path_no_attacks):
    return pd.read_csv(path_no_attacks)



def clean_first_line_dataset(path_in,path_out):
    input_file  = open(path_in, 'r')
    output_file = open(path_out, 'w')
    
    input_file.readline()
    line = input_file.readline()
    while line:
        word_list = line.split(',')
        attrib = ', '.join(word_list[1:])
        output_file.write(attrib)
        #output_file.write('\n')
        line=input_file.readline()
    output_file.close()

if __name__ == '__main__':
    a=read_dataset(ruta_cursos_iteracciones_modulo)
    a.drop(a.columns[[0]], axis=1, inplace=True)
    clean_first_line_dataset(ruta_cursos_iteracciones_modulo,ruta_cursos_iteracciones_modulo_preprocesado)
    
