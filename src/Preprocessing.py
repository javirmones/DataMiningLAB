#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime as dt
import Paths as route_of

def read_dataset(path):
    return pd.read_csv(path)
  
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
    
def preprocess_interactions_dates(route_interactions, route_output):
    file_in     = open(route_interactions, 'r')
    file_out    = open(route_output, 'w')
    
    file_out.write(file_in.readline())
    line = file_in.readline()
    
    while line:
        line_components     = line.split(',')
        line_components[2]  = line_components[2].split('T')[0]
        line_to_write = ','.join(map(str, line_components))
        
        file_out.write(line_to_write)
        line = file_in.readline()


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
  
def calculate_dropouts_and_finished_by_course(df_labeled, df_courses):
    
    df_courses['n_drops']               = 0
    df_courses['n_finished']            = 0
    df_courses['dropout_percentage']    = 0
    
    for course in df_courses['course_id']:
        df_drops  = df_labeled[(df_labeled.course_id == course) & (df_labeled.finished_course == 0)]
        df_finish = df_labeled[(df_labeled.course_id == course) & (df_labeled.finished_course == 1)]
        
        index = df_courses[(df_courses.course_id == course)].index
        df_courses.iloc[index, 3] = len(df_drops)
        df_courses.iloc[index, 4] = len(df_finish)
        df_courses.iloc[index, 5] = (len(df_drops) / (len(df_drops) + len(df_finish)))
        
  
        
def combine_datasets_to_target_data(courses_date, courses_submodules_by_type, courses_events_by_type):
    
    data_target_2   = courses_date.merge(courses_submodules_by_type, on='course_id')
    data_target_3   = data_target_2.merge(courses_events_by_type, on='course_id')
    
    data_target_3['duration_in_days'] = 0
    for index in range(len(data_target_3)):
        date_from = calculate_ending_date(data_target_3.iloc[index, 1])
        date_to   = calculate_ending_date(data_target_3.iloc[index, 2])
        
        duration = date_to - date_from
        data_target_3.iloc[index, 28] = duration.days
    
    return data_target_3

if __name__ == '__main__':
  
  categories = ['about', 'chapter', 'course', 'course_info', 'html',
                  'outlink', 'problem', 'sequential', 'static_tab',
                  'vertical', 'video', 'combinedopenended', 'peergrading',
                  'discussion', 'dictation']
  fechas_curso                  = read_dataset(route_of.date_courses)
  ultima_interaccion_cursos     = read_dataset(route_of.last_interaction)
  cursos_usuario                = read_dataset(route_of.enrollment_data)
  interacciones_usuario         = read_dataset(route_of.data_interactions)
  
  submodulos_por_tipo_y_curso   = read_dataset(route_of.course_types_modules)
  eventos_por_tipo_y_curso      = read_dataset(route_of.course_types_events)
  
  log_enrollment                = interacciones_usuario.merge(cursos_usuario, on='enrollment_id')  
  to_csv(route_of.interactions_enrollment, log_enrollment)
  
  labeling_dropouts(log_enrollment, fechas_curso, cursos_usuario)
  calculate_dropouts_and_finished_by_course(cursos_usuario, fechas_curso)
  
  to_csv(route_of.labeling_dropout, cursos_usuario)
  to_csv(route_of.users_drop_and_finished_by_course, fechas_curso)
  
  data_target = combine_datasets_to_target_data(fechas_curso, submodulos_por_tipo_y_curso, eventos_por_tipo_y_curso)
  to_csv(route_of.target_data, data_target)
#  preprocess_interactions_dates(route_of.interactions_enrollment, route_of.interactions_enrollment_def)
