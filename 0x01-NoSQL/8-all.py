#!/usr/bin/env python3

def list_all(mongo_collection):
    return [doc for doc in mongo_collection.find()]
