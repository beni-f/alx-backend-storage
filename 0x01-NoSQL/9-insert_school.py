#!/usr/bin/env python3
"""
    9-insert_school
"""


def insert_school(mongo_collection, **kwargs):
    result = mongo_collection.insertOne(kwargs)
    return result._id