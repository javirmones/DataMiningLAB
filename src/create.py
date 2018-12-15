#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import Paths as route_of

from Database import DatabaseKDD 

def write_from_list(feature_list_string, elements_list, path_out):
    output_file  = open(path_out, 'w')
    
    output_file.write(feature_list_string)
    for list_to_write in elements_list:
        line_to_write = ', '.join(map(str, list_to_write))
        output_file.write(line_to_write+"\n")
        
class CreationWizard():

    def __init__(self):
        self.db = DatabaseKDD()

    def create_dataframes(self):
      
        module_last_activity_query     = self.db.query("SELECT DISTINCT(t1.enrollment_id), t1.object, MAX(t1.time) AS time, t2.username, t2.course_id\nFROM log_train AS t1\nJOIN enrollment_train AS t2 on t1.enrollment_id = t2.enrollment_id\nGROUP BY t1.enrollment_id\nORDER BY t1.enrollment_id;")
        module_last_activity_list      = [list(enrollment_id) for enrollment_id in module_last_activity_query]
        write_from_list("enrollment_id,object,time,username,course\n", module_last_activity_list, route_of.last_interaction)        

#        log_train_course_users_query   = self.db.query("SELECT t1.enrollment_id, t2.username, t2.course_id, t1.object, t1.time, t1.source, t1.event\nFROM log_train AS t1\nJOIN enrollment_train AS t2 on t1.enrollment_id = t2.enrollment_id")
#        log_train_course_users_list   = [list(enrollment_id) for enrollment_id in log_train_course_users_query]
#        write_from_list("enrollment_id,username,course_id,object,time,source,event\n", log_train_course_users_list, route_of.data_interactions)        

        course_module_query     = self.db.query("SELECT DISTINCT(module_id),course_id\nFROM objets\nGROUP BY module_id;")
        course_module_list      = [list(course_id) for course_id in course_module_query]
        write_from_list("module_id,course_id\n", course_module_list, route_of.modules_by_course)
        
        module_activity_query     = self.db.query("SELECT DISTINCT(t1.enrollment_id), t1.object, COUNT(t1.object) AS interactions, t1.event AS event, t1.source AS source, t2.course_id, t2.username\nFROM log_train AS t1\nJOIN enrollment_train AS t2 on t1.enrollment_id = t2.enrollment_id\nGROUP BY t1.object\nORDER BY t1.enrollment_id;")
        module_activity_list      = [list(enrollment_id) for enrollment_id in module_activity_query]
        write_from_list("enrollment_id,object,interactions,event,source,course_id,username\n", module_activity_list, route_of.total_interaction)        
                        
    def main(self):
        self.create_dataframes()


if __name__ == '__main__':
    
    merlin = CreationWizard()
    merlin.main()
    