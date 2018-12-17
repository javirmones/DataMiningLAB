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
  
def calculate_dropouts_and_finished_by_course(df_labeled, df_courses):
    
    df_courses['n_drops']       = 0
    df_courses['n_finished']    = 0
    
    for course in df_courses['course_id']:
        df_drops  = df_labeled[(df_labeled.course_id == course) & (df_labeled.finished_course == 0)]
        df_finish = df_labeled[(df_labeled.course_id == course) & (df_labeled.finished_course == 1)]
        
        index = df_courses[(df_courses.course_id == course)].index
        df_courses.iloc[index, 3] = len(df_drops)
        df_courses.iloc[index, 4] = len(df_finish)
  

def assign_number_submodules_by_type_and_course(category_list, df_course):
    
    for category in category_list:
        df_category     = read_dataset(route_of.target_data_category.format(category))
        
        for course in df_course['course_id']:
            if (len(df_category[(df_category.course_id == course)])) <= 0:
                aux = pd.DataFrame([[course, 0]], [len(df_category)], ['course_id', 'number_of_{}'.format(category)])
                df_category = pd.concat([df_category,aux])
        
        to_csv(route_of.target_data_category.format(category), df_category)
        
def combine_datasets_to_target_data(categories):
    
    data_target_users_per_course        = read_dataset(route_of.users_per_course)
    data_target_courses_date            = read_dataset(route_of.date_courses)
    data_target_submodules_total        = read_dataset(route_of.number_submodules_by_courses)
    
    data_target_2   = data_target_users_per_course.merge(data_target_courses_date, on='course_id')
    data_target_3   = data_target_2.merge(data_target_submodules_total, on='course_id')
    
    for category in categories:
        df_category     = read_dataset(route_of.target_data_category.format(category))
        data_target_3   = data_target_3.merge(df_category, on='course_id')

    return data_target_3

    # TO DO CONTAR USUARIOS ABANDONO EN METODO APARTE Y UNIR TODOS LOS DATASETS

if __name__ == '__main__':
  
  categories = ['about', 'chapter', 'course', 'course_info', 'html',
                  'outlink', 'problem', 'sequential', 'static_tab',
                  'vertical', 'video', 'combinedopenended', 'peergrading',
                  'discussion', 'dictation']
#  fechas_curso                  = read_dataset(route_of.date_courses)
#  ultima_interaccion_cursos     = read_dataset(route_of.last_interaction)
#  cursos_usuario                = read_dataset(route_of.enrollment_data)
#  interacciones_usuario         = read_dataset(route_of.data_interactions)
#  interacciones_usuario_module  = read_dataset(route_of.total_interaction)
#  
#  log_enrollment                = cursos_usuario.merge(interacciones_usuario, on='enrollment_id')  
#  
#  labeling_dropouts(log_enrollment, fechas_curso, cursos_usuario)
#  calculate_dropouts_and_finished_by_course(cursos_usuario, fechas_curso)
#  
#  to_csv(route_of.labeling_dropout, cursos_usuario)
#  to_csv(route_of.users_drop_and_finished_by_course, fechas_curso)
  
  assign_number_submodules_by_type_and_course(categories, fechas_curso)
  data_target = combine_datasets_to_target_data(categories)
  