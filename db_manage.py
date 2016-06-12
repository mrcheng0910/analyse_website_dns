#encoding:utf-8
"""
数据库操作
"""

from pymongo import MongoClient
import pymongo
from datetime import datetime,timedelta


def get_db():
    """
    获取数据库
    :return:
    其他：可以完善
    """
    client = MongoClient()
    db = client.websites_dns
    return db

def insert(coll_name=None,pkt_count=0, detail=None):
    """
    插入数据
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
    # print "result.inserted_id: {}".format(result.inserted_id)


# Insert('google.com')
#
# def FindNames():
#     client = MongoClient()
#     db = client.test
#     # A chamada find serve para buscar informação, ela retorna um cursor para o
#     # primeiro rsultado da busca e pode ser iterado
#     cursor = db.restaurants.find({}, ["name"])
#     for document in cursor:
#         print(document)
#
#
# def FindAll():
#     client = MongoClient()
#     db = client.test
#     # A chamada find serve para buscar informação, ela retorna um cursor para o
#     # primeiro rsultado da busca e pode ser iterado
#     cursor = db.restaurants.find()
#     for document in cursor:
#         print(document)
#
#
# def FindCount():
#     client = MongoClient()
#     db = client.test
#     # para descobrir a quantdiade de resultados existe a funcao count()
#     cursor = db.restaurants.find()
#     cursor.count()
#
#
# def FindeQuery():
#     client = MongoClient()
#     db = client.test
#     # Para filtrar os resultados envie um objeto com os parametros que deseja buscar
#     cursor = db.restaurants.find({"address.zipcode": "10075"})
#     for document in cursor:
#         print(document)
#     print len(cursor)
#
#
# def FindeQueryArray():
#     client = MongoClient()
#     db = client.test
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
#     db = client.test
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
#     db = client.test
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
#     db = client.test
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
#     db = client.test
#     result = db.restaurants.delete_many({"name": ""})
#     print "{} restaurantes destroyed".format(result.deleted_count)
#     print ("Everybody has a name!")
#     print db.restaurants.find({"name": ""}).count()
#
#
# def DestroyManhattan():
#     client = MongoClient()
#     db = client.test
#     result = db.restaurants.delete_many({"borough": "Manhattan"})
#     print "{} restaurantes destroyed".format(result.deleted_count)
#     print ("No more food in manhattan!")
#
# def CreateCousineIndex():
#     client = MongoClient()
#     db = client.test
#     db.restaurants.create_index([("cuisine", pymongo.ASCENDING)])
#
# def CreateBoroughNameIndex():
#     client = MongoClient()
#     db = client.test
#     db.restaurants.create_index([("borough", pymongo.ASCENDING),("adress.zipcode",pymongo.ASCENDING)])
#
# def CreateUniqueRestaurantIdIndex():
#     client = MongoClient()
#     db = client.test
#     db.restaurants.create_index([("restaurant_id", pymongo.ASCENDING)],unique=True)
#
# def AddDuplicateNumberID():
#     client = MongoClient()
#     db = client.test
#     db.restaurants.insert_one({"restaurant_id":"50018995"})
#
# def FindRedundantNames():
#     client = MongoClient()
#     db = client.test
#     cursor = db.restaurants.aggregate(
#         [
#             {"$group": {"_id": "$name", "count": {"$sum": 1}}},
#             {"$sort": {"count": 1}}
#         ])
#     for document in cursor:
#         print(document)





