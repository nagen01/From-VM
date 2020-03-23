# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#Importing python arango library
from arango import ArangoClient

#Initializing arango client
client = ArangoClient(hosts = 'http://localhost:8529')

#Connect _system database, This gives access to root user
db = client.db('test', username = 'nagendra', password = '1432')

#Finding list of graphs present in test dataset
db.graphs()
