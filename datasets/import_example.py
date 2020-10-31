import redis
import json


class RedisTT(object):


    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 6379
        self.r = redis.StrictRedis(host=self.host, port=self.port, db=0)

    def insertRedis(self, keyName, jsonStr):
        self.r.lpush(keyName, jsonStr)


def save1():
    someexpert = {'id': 1000, 'realname': 'buaa'}
    if RedisTT().r.exists('someexpert'):
        RedisTT().r.delete('someexpert')
    RedisTT().insertRedis(keyName='someexpert', jsonStr=json.dumps(someexpert))


if __name__ == "__main__":
    save1()

print(RedisTT().r.lrange('someexpert', 0, RedisTT().r.llen('someexpert')))
