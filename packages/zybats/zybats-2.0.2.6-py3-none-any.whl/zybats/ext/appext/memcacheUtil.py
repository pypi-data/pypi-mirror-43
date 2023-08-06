from pymemcache.client.base import Client
from pymemcache.client.hash import HashClient

class MemcacheCli(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = Client((self.host, self.port))

    def set(self,key,value,expire):
        try:
            return self.client.set(key,value,expire)
        except Exception as e:
            return False
    def get(self,key):
        try:
            return self.client.get(key,default=None)
        except Exception as e:
            return None
    def mset(self,values,expire):
        try:
            return self.client.set_many(values,expire)
        except Exception as e:
            return False
    def mget(self,keys):
        try:
            return self.client.get_many(keys)
        except Exception as e:
            return None

class MemcacheHashCli(object):


    def __init__(self, hosts):
        self.client = HashClient(hosts)

    def set(self,key,value,expire):
        try:
            return self.client.set(key,value,expire)
        except Exception as e:
            return False
    def get(self,key):
        try:
            return self.client.get(key,default=None)
        except Exception as e:
            return None
    def mset(self,values,expire):
        try:
            return self.client.set_many(values,expire)
        except Exception as e:
            return False
    def mget(self,keys):
        try:
            return self.client.get_many(keys)
        except Exception as e:
            return None


if __name__=='__main__':
    mm=MemcacheCli("192.168.240.31",18087)
    mm.set('age',10,60)
    hosts=[('192.168.240.31',18087),('192.168.240.32',18087)]
    mm=MemcacheHashCli(hosts)