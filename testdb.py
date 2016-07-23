# encoding:utf-8
"""
数据库操作
"""

from pymongo import MongoClient
import pymongo
from datetime import datetime,timedelta,date
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


def get_domain_info(domain=None,start_date=datetime.utcnow()+ timedelta(hours=8),end_date=datetime.utcnow()+timedelta(hours=8)):
    """
    获取指定域名和日期的探测数据，根据开始日期和结束日期，从数据库中获取当天数据
    :param domain: 域名
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return:
    """
    if start_date.date() == end_date.date():    # 获得域名的当天探测数据
        domain_collection = get_domain_collection(domain)
        return domain_collection.find({'visit_time':{'$lte':end_date,'$gte':start_date.replace(hour=0,minute=0,second=0,microsecond=0)}})

    # print get_domain_collection('baidu.com')


def extract_domain_field_info(domain_dns_pkt = None):
    """

    :return:
    """
    if domain_dns_pkt is None:
        return
    for pkt in domain_dns_pkt:
        print pkt['pkt_count'],pkt['visit_time']



a = get_domain_info('baidu.com')
extract_domain_field_info(a)


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


# def FindNames():
#     client = MongoClient()
#     db = client.drawTable
#     # A chamada find serve para buscar informação, ela retorna um cursor para o
#     # primeiro rsultado da busca e pode ser iterado
#     cursor = db.restaurants.find({}, ["name"])
#     for document in cursor:
#         print(document)
#
#
# def FindAll():
#     client = MongoClient()
#     db = client.drawTable
#     # A chamada find serve para buscar informação, ela retorna um cursor para o
#     # primeiro rsultado da busca e pode ser iterado
#     cursor = db.restaurants.find()
#     for document in cursor:
#         print(document)
#
#
# def FindCount():
#     client = MongoClient()
#     db = client.drawTable
#     # para descobrir a quantdiade de resultados existe a funcao count()
#     cursor = db.restaurants.find()
#     cursor.count()
#
#
# def FindeQuery():
#     client = MongoClient()
#     db = client.drawTable
#     # Para filtrar os resultados envie um objeto com os parametros que deseja buscar
#     cursor = db.restaurants.find({"address.zipcode": "10075"})
#     for document in cursor:
#         print(document)
#     print len(cursor)
#
#
# def FindeQueryArray():
#     client = MongoClient()
#     db = client.drawTable
#     # É possivel filtrar por parametros contidos em um vetor interno
#     # o resultado vai conter todos os documentos em que algum elemento do vetor
#     # satisfizer o filtro
#     cursor = db.restaurants.find({"grades.grade": "B"})
#     for document in cursor:
#         print(document)
#
#
# def ComplexQuery():
#     client = MongoClient()
#     db = client.drawTable
#     cursor = db.restaurants.find({
#         "$or": [{
#             "grades.score": {
#                 "$lt": 100
#             },
#             "grades.score": {
#                 "$gt": 90
#             },
#             "borough": "Manhattan"
#         }, {
#             "grades.score": {
#                 "$in": [50, 40]
#             },
#             "borough": "Staten Island"
#         }]
#     }).sort([
#         ("borough", pymongo.ASCENDING)
#     ])
#     for document in cursor:
#         print(document)
#     print "cursor.count()={}".format(cursor.count())
#
# def UpdateUndefinedCategory():
#     client = MongoClient()
#     db = client.drawTable
#     result = db.restaurants.update_many(
#         {"address.zipcode": "10016", "cuisine": "Other"},
#         {
#             "$set": {"cuisine": "Category To Be Determined"}
#         })
#     print "{} restaurants matched.".format(result.matched_count)
#     # print "{} restaurants modified.".format(result.modified_count)
#
#
# def RestaurantsByBorough():
#     client = MongoClient()
#     db = client.drawTable
#     cursor = db.restaurants.aggregate(
#         [
#             {"$group": {"_id": "$borough", "count": {"$sum": 1}}},
#             {"$sort": {"_id": 1}}
#         ])
#     for document in cursor:
#         print(document)
#
#
# def DestroyThoseWhoCannotBeNamed():
#     client = MongoClient()
#     db = client.drawTable
#     result = db.restaurants.delete_many({"name": ""})
#     print "{} restaurantes destroyed".format(result.deleted_count)
#     print ("Everybody has a name!")
#     print db.restaurants.find({"name": ""}).count()
#
#
# def DestroyManhattan():
#     client = MongoClient()
#     db = client.drawTable
#     result = db.restaurants.delete_many({"borough": "Manhattan"})
#     print "{} restaurantes destroyed".format(result.deleted_count)
#     print ("No more food in manhattan!")
#
# def CreateCousineIndex():
#     client = MongoClient()
#     db = client.drawTable
#     db.restaurants.create_index([("cuisine", pymongo.ASCENDING)])
#
# def CreateBoroughNameIndex():
#     client = MongoClient()
#     db = client.drawTable
#     db.restaurants.create_index([("borough", pymongo.ASCENDING),("adress.zipcode",pymongo.ASCENDING)])
#
# def CreateUniqueRestaurantIdIndex():
#     client = MongoClient()
#     db = client.drawTable
#     db.restaurants.create_index([("restaurant_id", pymongo.ASCENDING)],unique=True)
#
# def AddDuplicateNumberID():
#     client = MongoClient()
#     db = client.drawTable
#     db.restaurants.insert_one({"restaurant_id":"50018995"})
#
# def FindRedundantNames():
#     client = MongoClient()
#     db = client.drawTable
#     cursor = db.restaurants.aggregate(
#         [
#             {"$group": {"_id": "$name", "count": {"$sum": 1}}},
#             {"$sort": {"count": 1}}
#         ])
#     for document in cursor:
#         print(document)





