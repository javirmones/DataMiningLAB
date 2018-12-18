#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import Paths as route_of

from Database import DatabaseKDD 
from CreationWizard import CreationWizard

def write_from_list(feature_list_string, elements_list, path_out):
    output_file  = open(path_out, 'w')
    
    output_file.write(feature_list_string)
    for list_to_write in elements_list:
        line_to_write = ', '.join(map(str, list_to_write))
        output_file.write(line_to_write+"\n")

def to_csv(path, source):
    source.to_csv(path)

class App():

    def __init__(self):

        self.db = DatabaseKDD()

    def create_dataframes(self):
        '''
        #students_query      = self.db.query("SELECT COUNT(DISTINCT username) FROM enrollment_train")
        module_last_activity_query  = self.db.query("SELECT enrollment_id, object, MAX(time) AS time\nFROM log_train\nGROUP BY enrollment_id\nORDER BY enrollment_id;")
        module_last_activity_list   = [list(enrollment_id) for enrollment_id in module_last_activity_query]
        write_from_list("enrollment_id,object,time\n", module_last_activity_list, route_of.last_interaction)        

        course_id_query             = self.db.query("SELECT DISTINCT(course_id) FROM objets;")
        course_id_list              = [list(course_id) for course_id in course_id_query]
        course_id_df                = pd.DataFrame(course_id_list, columns = ['course_id'])

        courses_query               = self.db.query("SELECT DISTINCT(module_id) FROM objets;")
        courses_list                = [list(course) for course in courses_query]
        courses_df                  = pd.DataFrame(courses_list, columns = ['module_id'])

        users_query                 = self.db.query("SELECT DISTINCT(username) from enrollment_train;")
        users_list                  = [list(user) for user in users_query]
        users_df                    =  pd.DataFrame(users_list, columns = ['users'])

        interactions_query          = self.db.query("SELECT t1.course_id, COUNT(username)\nFROM date AS t1\nJOIN enrollment_train AS t2 on t1.course_id = t2.course_id\nGROUP BY t1.course_id;")
        interactions_list           = [list(interactions) for interactions in interactions_query]
        interactions_df             = pd.DataFrame(interactions_list, columns = ['course_id', 'users_by_course'])
        
        module_activity_query       = self.db.query("SELECT DISTINCT(t1.enrollment_id), t1.object, COUNT(t1.object) AS interactions, t1.event AS event, t1.source AS source, t2.course_id, t2.username\nFROM log_train AS t1\nJOIN enrollment_train AS t2 on t1.enrollment_id = t2.enrollment_id\nGROUP BY t1.object\nORDER BY t1.enrollment_id;")
        module_activity_list        = [list(enrollment_id) for enrollment_id in module_activity_query]
        #modele_activity_df        = pd.DataFrame(interactions_list, columns = ['enrollment_id', 'module', 'interactions', 'course_id', 'username'])
        write_from_list("enrollment_id,object,interactions,event,source,course_id,username\n", module_activity_list, route_of.total_interaction)        

        final_df                    = pd.concat([course_id_df, users_df], axis = 1, join_axes = [course_id_df.index])
        final_df                    = pd.concat([final_df, courses_df], axis = 1, join_axes = [final_df.index])
        final_df                    = pd.merge(final_df, interactions_df, on='course_id') # REVISAR
    
        to_csv(route_of.user_interactions, final_df)
        '''
        merlin = CreationWizard()
        merlin.create_dataframes()

    def main(self):
        self.create_dataframes()


if __name__ == '__main__':
    
    app = App()
    app.main()
    

