import redis
from rediscluster import StrictRedisCluster

class RedisSingleNode(object):
    def __init__(self, ip, port):
        self.host = ip
        self.port = port
        self.__connect()

    #析构函数，断开连接
    def __del__(self):
        if self.connect:
            self.connect.connection_pool.disconnect()

    def __connect(self):
        try:
            pool = redis.ConnectionPool(host=self.host, port=self.port)
            self.connect = redis.Redis(connection_pool=pool)
        except Exception as e:
            self.connect = None
            print("Connect redis error!", e)
            return


    #set方法
    def set(self, key, value):
        try:
            self.connect.set(key, value)
            return True
        except Exception as e:
            print("RedisUtil excute set method failed!", e)
            return  False


    #get方法
    def get(self, key):
        try:
            return self.connect.get(key)
        except Exception as e:
            print("RedisUtil excute get method failed!", e)
            return None
    #del方法
    def delete(self, key):
        try:
            self.connect.delete(key)
            return True
        except Exception as e:
            print("RedisUtil excute delete method failed!", e)
            return False
    #mset方法
    def mset(self, map):
        try:
            self.connect.mset(map)
            return True
        except Exception as e:
            print("RedisUtil excute mset method failed!", e)
            return False

    #mget方法
    def mget(self, array_keys):
        try:
            return self.connect.mget(array_keys)
        except Exception as e:
            print("RedisUtil excute mget method failed!", e)
            return None
    #hset方法
    def hset(self, key, field, value):
        try:
            self.connect.hset(key, field, value)
            return True
        except Exception as e:
            print("RedisUtil excute hset method failed!", e)
            return False
    #hget方法
    def hget(self, key, field):
        try:
            return self.connect.hget(key, field)
        except Exception as e:
            print("RedisUtil excute hget method failed!", e)
            return None


class RedisClusterNode(object):
    def __init__(self, node_list):
        self.node_list = node_list
        self.__connect()

    #析构函数，断开连接
    def __del__(self):
        if self.connect:
            pass

    def __connect(self):
        try:
            self.connect = StrictRedisCluster(startup_nodes=self.node_list)
        except Exception as e:
            self.connect = None
            print("Connect redisCluster node error!", e)
            return


    #set方法
    def set(self, key, value):
        try:
            self.connect.set(key, value)
            return True
        except Exception as e:
            print("RedisUtil excute set method failed!", e)
            return  False


    #get方法
    def get(self, key):
        try:
            return self.connect.get(key)
        except Exception as e:
            print("RedisUtil excute get method failed!", e)
            return None
    #del方法
    def delete(self, key):
        try:
            self.connect.delete(key)
            return True
        except Exception as e:
            print("RedisUtil excute delete method failed!", e)
            return False
    #mset方法
    def mset(self, map):
        try:
            self.connect.mset(map)
            return True
        except Exception as e:
            print("RedisUtil excute mset method failed!", e)
            return False

    #mget方法
    def mget(self, array_keys):
        try:
            return self.connect.mget(array_keys)
        except Exception as e:
            print("RedisUtil excute mget method failed!", e)
            return None
    #hset方法
    def hset(self, key, field, value):
        try:
            self.connect.hset(key, field, value)
            return True
        except Exception as e:
            print("RedisUtil excute hset method failed!", e)
            return False
    #hget方法
    def hget(self, key, field):
        try:
            return self.connect.hget(key, field)
        except Exception as e:
            print("RedisUtil excute hget method failed!", e)
            return None

if __name__ =='__main__':
    #r = RedisSingleNode('192.168.240.98', 6379)
    redis_nodes = [{'host': '192.168.240.98', 'port': 50010},
                   {'host': '192.168.240.98', 'port': 50011},
                   {'host': '192.168.240.98', 'port': 50012}]
    r = RedisClusterNode(redis_nodes)
    r.set("1111", "2222")
    print(r.get("11112"))

    map_param = {"666": "6v", "777": 77}
    r.mset(map_param)
    print(r.mget(["1111", "666", "777"]))
