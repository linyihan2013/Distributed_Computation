__author__ = 'linyihan'
import redis

r = redis.Redis()

r.set("mykey", "somevalue")
print(r.get("mykey"))

r.set("mykey", "newvalue", xx=1)
print(r.get("mykey"))

r.set("counter", 100)
r.incr("counter")
print(r.get("counter"))

r.incr("counter", 50)
print(r.get("counter"))

set1 = {"a": 1, "b": 2, "c": 3}
r.mset(set1)
print(r.mget(set1))

print(r.exists("mykey"))
r.delete("mykey")
print(r.exists("mykey"))

r.set("mykey", "x")
print(r.type("mykey"))
r.delete("mykey")
print(r.type("mykey"))

print(r.rpush("mylist", "A"))
print(r.rpush("mylist", "B"))
print(r.lpush("mylist", "first"))
print(r.lrange("mylist", 0, -1))

print(r.hmset("user:1000", {"username": "antirez", "birthyear": 1995, "verified": 1}))
print(r.hmget("user:1000", "username"))
print(r.hmget("user:1000", "birthyear"))
print(r.hincrby("user:1000", "birthyear", 50))

print(r.sadd("myset", 1, 2, 3))
print(r.smembers("myset"))
print(r.sismember("myset", 1))