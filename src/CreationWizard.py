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
        
    print('file saved correctly at {}'.format(path_out))
        
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
        
        target_data_course_submodules_query     = self.db.query("SELECT course_id, COUNT(module_id) AS n_submodules\nFROM objets2\nGROUP BY course_id")
        target_data_course_submodules_list      = [list(course_id) for course_id in target_data_course_submodules_query]
        write_from_list("course_id, n_submodules_total\n", target_data_course_submodules_list, route_of.number_submodules_by_courses)

        users_per_course_query                  = self.db.query("SELECT course_id, COUNT(username) FROM enrollment_train GROUP BY course_id")
        users_per_course_list                   = [list(course_users) for course_users in users_per_course_query]
        write_from_list("course_id, users_count\n", users_per_course_list, route_of.users_per_course)
        
        course_modules_type_query                  = self.db.query("SELECT a.course_id, SUM(b.access) AS number_access, SUM(b.navigate) AS number_navigates, SUM(b.problem) AS number_problems, SUM(b.page_close) AS number_pages_closes, SUM(b.video) AS number_videos, SUM(b.discussion) AS number_discussions, SUM(b.wiki) AS number_wikis\nFROM objets AS A\nJOIN(\nSELECT object, SUM(event='access') AS access,SUM(event='navigate') AS navigate,SUM(event='problem') AS problem,SUM(event='page_close') AS page_close,SUM(event='video') AS video,SUM(event='discussion') AS discussion,SUM(event='wiki') AS wiki\nFROM log_train\nGROUP BY object) b ON a.module_id = b.object\nGROUP BY a.course_id;")
        course_events_type_list                    = [list(course_id) for course_id in course_modules_type_query]
        write_from_list("course_id,n_access,n_navigates,n_problems,n_page_close,n_reproductions,n_discussions,n_wikis\n", course_events_type_list, route_of.course_types_events)
        
        course_modules_type_query                  = self.db.query("SELECT course_id, SUM(category='about') , SUM(category='chapter'), SUM(category='course'), SUM(category='course_info'), SUM(category='html'), SUM(category='outlink'), SUM(category='problem'),SUM(category='sequential'),SUM(category='static_tab'),SUM(category='vertical'),SUM(category='video'),SUM(category='combinedopened'),SUM(category='peergrading'),SUM(category='discussion'),SUM(category='dictation')\nFROM objets\nGROUP BY course_id;")
        course_modules_type_list                   = [list(course_id) for course_id in course_modules_type_query]
        write_from_list("course_id,about,chapter,course,course_info,html,outlink,problem,sequential,static_tab,vertical,video,combinedopened,peergrading,discussion,dictation\n", course_modules_type_list, route_of.course_types_modules)


    def main(self):
        self.create_dataframes()


if __name__ == '__main__':
    
    merlin = CreationWizard()
    merlin.main()
    