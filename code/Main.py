#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import Paths as route_of

from Database import DatabaseKDD 


def to_csv(path, source):
    source.to_csv(path)

class App():

    def __init__(self):

        self.db = DatabaseKDD()

    def create_dataframes(self):
        
        #students_query      = self.db.query("SELECT COUNT(DISTINCT username) FROM enrollment_train")        
        course_id_query     = self.db.query("SELECT DISTINCT(course_id) FROM objets;")
        course_id_list      = [list(course_id) for course_id in course_id_query]
        course_id_df        = pd.DataFrame(course_id_list, columns = ['course_id'])

        courses_query       = self.db.query("SELECT DISTINCT(module_id) FROM objets;")
        courses_list        = [list(course) for course in courses_query]
        courses_df          = pd.DataFrame(courses_list, columns = ['course'])

        users_query         = self.db.query("SELECT DISTINCT(username) from enrollment_train")
        users_list          = [list(user) for user in users_query]
        users_df            =  pd.DataFrame(users_list, columns = ['users'])

        interactions_query  = self.db.query("SELECT t1.course_id, COUNT(username)\nFROM date AS t1\nJOIN enrollment_train AS t2 on t1.course_id = t2.course_id\nGROUP BY t1.course_id;")
        interactions_list   = [list(interactions) for interactions in interactions_query]
        interactions_df     = pd.DataFrame(interactions_list, columns = ['course_id', 'course_interactions'])

        final_df            = pd.concat([course_id_df, users_df], axis = 1, join_axes = [course_id_df.index])
        final_df            = pd.concat([final_df, courses_df], axis = 1, join_axes = [final_df.index])
        final_df            = pd.concat([final_df, interactions_df], axis = 1, join_axes = [final_df.index] )
    
        to_csv(route_of.user_interactions, final_df)
    
    def main(self):
        self.create_dataframes()


if __name__ == '__main__':
    
    app = App()
    app.main()
