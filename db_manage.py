# encoding:utf-8
"""
数据库操作
"""

from pymongo import MongoClient
from datetime import datetime,timedelta
import tldextract


def get_db():
    """
    获取数据库
    :return
    其他：可以完善
    """
    client = MongoClient()
    db = client.websites_dns
    return db


def extract_domain_of_url(url=None):
    """
    url中提取出domain
    :param url:网址
    :return
    正常：返回domain
    异常：返回None
    """
    if url is None:
        return
    no_fetch_extract = tldextract.TLDExtract(suffix_list_urls=None)
    url = no_fetch_extract(url)
    if url.domain == "" or url.suffix == "":
        return
    else:
        return url.domain + '.' + url.suffix


def get_domain_collection(domain=None):
    """
    获取域名在数据库中对应的collection
    :param domain: 域名
    :return
    db.collection
    """
    if domain is None:
        return
    collection_name = domain.replace('.','_')
    db = get_db()
    return db[collection_name]


def find_domain_info(domain=None, datetime=None):
    # db = get_db()
    print get_domain_collection('baidu.com')


# find_domain_info()


def insert(coll_name=None,pkt_count=0, detail=None):
    """
    插入基础数据
    :param coll_name:
    :param pkt_count:
    :param detail:
    :return:
    """

    if coll_name == None or detail == None:
        return
    if pkt_count == 0:
        return
    coll_name = coll_name.replace('.','_')  # 使用"_"替换"."
    db = get_db()
    collection = db[coll_name]
    result = collection.insert_one(
        {
            "visit_time": datetime.utcnow() + timedelta(hours=8),  # 当前时区
            "pkt_count": pkt_count,
            "details":detail
        }
    )
    print "result.inserted_id: {}".format(result.inserted_id)


def insert_detect_dns():

    db = get_db()
    collection = db['detect_dns']
    data ={
        "detect_geo": "威海",
        "detect_network_operator": "联通",
        "dns": "223.5.5.5",
        "dns_geo": "杭州",
        "dns_network_operator": "阿里云"
    }

    result = collection.insert_one()
    print "result.inserted_id: {}".format(result.inserted_id)