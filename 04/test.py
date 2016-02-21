__author__ = 'yihan'
import pymongo
import hashlib

m = hashlib.md5()
m.update("123".encode())

conn = pymongo.MongoClient()
db = conn.example
users = db.users
users.insert({"name": "zixuan", "alias_name": "xuanxuan", "password": m.hexdigest()})
users.insert({"name": "yingjie", "alias_name": "jiejie", "password": m.hexdigest()})
users.insert({"name": "yihan", "alias_name": "hanhan", "password": m.hexdigest()})

admins = db.admins
admins.insert({"name": "zixuan", "alias_name": "xuanxuan", "password": m.hexdigest()})
admins.insert({"name": "yingjie", "alias_name": "jiejie", "password": m.hexdigest()})
admins.insert({"name": "yihan", "alias_name": "hanhan", "password": m.hexdigest()})

vips = db.vips
vips.insert({"name": "zixuan", "alias_name": "xuanxuan", "password": m.hexdigest()})
vips.insert({"name": "yingjie", "alias_name": "jiejie", "password": m.hexdigest()})
vips.insert({"name": "yihan", "alias_name": "hanhan", "password": m.hexdigest()})

cursor = users.find()
sum = 0
for doc in cursor:
    print(doc)