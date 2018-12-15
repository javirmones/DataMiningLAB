#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import Paths as route_of

def read_dataset(path_no_attacks):
    return pd.read_csv(path_no_attacks)
  
def labeling_dropouts(df_interactions, df_courses_date, df_courses_users):
  df_courses_users['finished_course']=0
    
  for i in range(len(df_courses_date)):
    print("------ CURSO {} ------".format(i))
    course    = df_courses_date.course_id[i].replace(" ", "")
    date_min  = df_courses_date.to[i]
    date_aux  = calculate_ending_date(df_courses_date.to[i])
    date_max  = "{}-{}-{}".format(date_aux.year, date_aux.month, date_aux.day)
    
    data_mov = df_interactions[(df_interactions.time > date_min) 
                                & (df_interactions.time <= date_max)
                                & (df_interactions.course_id == course)]
    for user_no_drop in pd.unique(data_mov['username']):
      index_user = df_courses_users[(df_courses_users.username == user_no_drop) 
                                    & (df_courses_users.course_id == course)].index
      df_courses_users.loc[index_user, 'finished_course'] = 1
      print(df_courses_users.iloc[index_user])
      print("**********************")
      
def calculate_ending_date(date_str):
  date_elements = date_str.split('-')
  
  date_def      = dt.date(int(date_elements[0]), int(date_elements[1]), int(date_elements[2]))
  date_def      = date_def + dt.timedelta(days=10) 
  
  return date_def

def to_csv(path,dataframe):
    dataframe.to_csv(path)
    print("File created sucessfully at: {}".format(path))

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
  
  fechas_curso                  = read_dataset(route_of.date_courses)
  ultima_interaccion_cursos     = read_dataset(route_of.last_interaction)
  cursos_usuario                = read_dataset(route_of.enrollment_data)
  interacciones_usuario         = read_dataset(route_of.data_interactions)
  
  log_enrollment                = cursos_usuario.merge(interacciones_usuario, on='enrollment_id')  
  to_csv(route_of.labeling_dropout, cursos_usuario)
  
  labeling_dropouts(log_enrollment, fechas_curso, cursos_usuario)
