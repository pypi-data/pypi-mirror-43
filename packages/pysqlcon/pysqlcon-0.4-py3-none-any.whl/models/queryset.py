"""
@author: Kudzai Tsapo (kudzai@charteredsys.com)

Description: 
--------------
This file contains the classes for Querying the database
"""
from string import Template
import os

class Row(object):

    def __init__(self, fields, table):
        pass

class Column(object):
    def __init__(self, *args):
        self.sql_statement = ''
        for arg in args:
            self.sql_statement += str(arg) + ' '

    def __str__(self):
        return self.sql_statement

class Table(object):
    def __init__(self, name, properties=[]):
        if len(properties) == 0:
            raise TypeError("Missing columns")
        
        sql_filepath = os.path.join(os.path.dirname(__file__), 'sql', 'table_creation.sql')
        string_template = Template(open(sql_filepath, 'r').read())
        table_property = ''
        limit = len(properties) - 1
        for count in range(limit):
            table_property += str(properties[count]) + ','
        else:
            table_property += properties[limit]

        sql_string = string_template.substitute(tablename=name, properties=table_property)
        self.statement = sql_string




class Query:

    def __init__(self, query, query_type='raw', params=()):
        self.query = query
        self.query_type = query_type
        self.parameters = params


class Session(object):
    def __init__(self, connection_object):
        self.query = None
        self.connection = connection_object

    def add(self, query):
        if 'sp' in query.query_type.lower():
            self.connection.execute_procedure(query.query, query.parameters)
        else:
            self.connection.execute_query(query.query, query.parameters)

    def query(self, query):
        if 'sp' in query.query_type.lower():
            self.connection.execute_procedure(query.query, query.parameters)
        else:
            self.connection.execute_query(query.query, query.parameters)

        return self.connection.fetch_rows()



