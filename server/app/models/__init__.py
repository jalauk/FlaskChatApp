from flask_mongoengine import MongoEngine
import redis

db = MongoEngine()

r = redis.Redis(
  host='redis-10105.c301.ap-south-1-1.ec2.cloud.redislabs.com',
  port=10105,
  password='NhmCObKVjrCgXZO29jJmCXAuGIbHt4eX')