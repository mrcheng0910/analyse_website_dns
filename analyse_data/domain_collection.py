# encoding:utf-8
"""
数据库操作
"""

from pymongo import MongoClient
from datetime import datetime,timedelta

def get_db():
    """
    获取数据库
    :return
    其他：可以完善
    """
    client = MongoClient()
    db = client.websites_dns
    return db


def get_domain_collection(domain=None):
    """
    获取域名在数据库中对应的collection
    :param domain: 域名
    :return
    db.collection
    """
    if domain is None:
        return
    collection_name = domain.replace('.', '_')
    db = get_db()
    return db[collection_name]


def insert(coll_name='data_info', result=None):
    """
    插入基础数据
    :param coll_name:
    :param pkt_count:
    :param result:
    :return:
    """

    if coll_name == None or result == None:
        return
    db = get_db()
    collection = db[coll_name]
    result = collection.insert_one(result)
    print "result.inserted_id: {}".format(result.inserted_id)
