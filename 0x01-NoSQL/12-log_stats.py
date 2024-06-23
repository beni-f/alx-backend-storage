#!/usr/bin/env python3
"""
    12-log_stats
"""
from pymongo import MongoClient

def print_request_logs(nginx_collection):
    """
       Provides some stats about Nginx logs stored in MongoDB 
    """
    print(f"{nginx_collection.count_documents({})} logs")
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    print("Methods:")
    for method in methods:
        print("\tmethod {}: {}".format(method, len(list(nginx_collection.find({"method": method})))))
    result = len(list(nginx_collection.find(
        {"method": "GET"},
        {"path": "/status"}
    )))
    print(f"{result} status check")



def run():
    '''Provides some stats about Nginx logs stored in MongoDB.
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_request_logs(client.logs.nginx)


if __name__ == '__main__':
    run()