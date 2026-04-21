import redis

r = redis.Redis(host="localhost", port=6379)
r.set("test_key", "hello", ex=60)
print(r.get("test_key"))