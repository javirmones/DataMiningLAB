#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy

import Paths

def read_dataset(path_no_attacks):
    return pd.read_csv(path_no_attacks)

def labeling_dropouts(df_last_inte, df_courses_users):
  pass

def clean_first_line_dataset(path_in,path_out):
    input_file  = open(path_in, 'r')
    output_file = open(path_out, 'w')
    
    input_file.readline()
    line = input_file.readline()
    while line:
        word_list = line.split(',')
        attrib = ', '.join(word_list[1:])
        output_file.write(attrib)
        line=input_file.readline()

    output_file.close()

if __name__ == '__main__':
    a=read_dataset(Paths.user_interactions)
    a.drop(a.columns[[0]], axis=1, inplace=True)
    clean_first_line_dataset(Paths.user_interactions, Paths.preprocessed_interactions)
    
