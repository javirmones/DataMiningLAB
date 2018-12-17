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

        module_last_activity_query              = self.db.query("SELECT DISTINCT(t1.enrollment_id), t1.object, MAX(t1.time) AS time, t2.username, t2.course_id\nFROM log_train AS t1\nJOIN enrollment_train AS t2 on t1.enrollment_id = t2.enrollment_id\nGROUP BY t1.enrollment_id\nORDER BY t1.enrollment_id;")
        module_last_activity_list               = [list(enrollment_id) for enrollment_id in module_last_activity_query]
        write_from_list("enrollment_id,object,time,username,course\n", module_last_activity_list, route_of.last_interaction)                        

        course_module_query                     = self.db.query("SELECT DISTINCT(module_id),course_id\nFROM objets\nGROUP BY module_id;")
        course_module_list                      = [list(course_id) for course_id in course_module_query]
        write_from_list("module_id,course_id\n", course_module_list, route_of.modules_by_course)
        
#        module_activity_query                   = self.db.query("SELECT DISTINCT(t1.enrollment_id), t1.object, COUNT(t1.object) AS interactions, t1.event AS event, t1.source AS source, t2.course_id, t2.username\nFROM log_train AS t1\nJOIN enrollment_train AS t2 on t1.enrollment_id = t2.enrollment_id\nGROUP BY t1.object\nORDER BY t1.enrollment_id;")
#        module_activity_list                    = [list(enrollment_id) for enrollment_id in module_activity_query]
#        write_from_list("enrollment_id,object,interactions,event,source,course_id,username\n", module_activity_list, route_of.total_interaction)        

        target_data_course_submodules_query     = self.db.query("SELECT course_id, COUNT(module_id) AS n_submodules\nFROM objets2\nGROUP BY course_id")
        target_data_course_submodules_list      = [list(course_id) for course_id in target_data_course_submodules_query]
        write_from_list("course_id, n_submodules_total\n", target_data_course_submodules_list, route_of.number_submodules_by_courses)
        
        categories_query        = self.db.query("SELECT DISTINCT(category)\nFROM objets")
        
        for category in categories_query.fetchall():
            target_data_category_module_query   = self.db.query("SELECT course_id, COUNT(category) AS number_category\nFROM objets2\nWHERE category='{}'\nGROUP BY course_id".format(category[0]))
            target_data_category_module_list    = [list(course_id) for course_id in target_data_category_module_query]
            write_from_list("course_id, number_of_{}\n".format(category[0]), target_data_category_module_list, route_of.target_data_category.format(category[0]))
            print(target_data_category_module_list)
        # TO DO: numero usuarios por curso, tipos de fuente por curso, usuarios abandono, usuarios no abandono
        users_per_course_query                  = self.db.query("SELECT course_id, COUNT(username) FROM enrollment_train GROUP BY course_id")
        users_per_course_list                   = [list(course_users) for course_users in users_per_course_query]
        write_from_list("course_id, users_count\n", users_per_course_list, route_of.users_per_course)


    def main(self):
        self.create_dataframes()


if __name__ == '__main__':
    
    merlin = CreationWizard()
    merlin.main()
    