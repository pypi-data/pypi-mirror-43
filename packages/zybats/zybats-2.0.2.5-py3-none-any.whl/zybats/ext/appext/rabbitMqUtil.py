import pika

class rabbitMqTool(object):
	# 构造函数，初始化连接
	def __init__(self, host, port, uname, passwd, exchange_type='fanout', durable=True):
		self.host = host
		self.port = port
		self.uname = uname
		self.passwd = passwd
		self.exchange_type = exchange_type
		self.durable = durable
		self.__connect()
	# 析构函数，断开连接
	def __del__(self):
		if self.connection:
			self.connection.close()
	def __connect(self):
		try:
			credentials = pika.PlainCredentials(self.uname, self.passwd)
			self.connection = pika.BlockingConnection(pika.ConnectionParameters(
				host=self.host, port=self.port, credentials=credentials))
		except Exception as e:
			print("Init connection to rabbitmq error!", e)
			return

		# channel.queue_declare(queue=BAP_INCREMENT_TODAY, durable=True)    #声明队列以向其发送消息消息

	# 生产消息方法
	def pushMsg(self, exchange, routing_key, msg):
		try:
			channel = self.connection.channel()
			channel.exchange_declare(exchange=exchange, exchange_type=self.exchange_type, durable=self.durable)
			channel.basic_publish(exchange=exchange, routing_key=routing_key, body=msg)
			return True
		except Exception as e:
			print("Push msg to rabbitmq error!", e)
			return False
	# 消费消息方法
	def pullMsg(self,  exchange, routing_key):
		def __callback(ch, method, properties, body):
			print("[消费者] this is an example, recv %s" % body)

		try:
			channel = self.connection.channel()
			channel.exchange_declare(exchange=exchange, exchange_type=self.exchange_type, durable=self.durable)
			queue_name = channel.queue_declare(exclusive=True).method.queue
			channel.queue_bind(exchange=exchange, queue=queue_name)
			channel.basic_consume(__callback, queue=queue_name)
			channel.start_consuming()
		except Exception as e:
			print("Pull msg from rabbitmq error!", e)

	# 定义一个回调函数，用来接收生产者发送的消息


if __name__ =='__main__':
	MQ_HOST = '192.168.240.99'
	MQ_PORT = 5672
	MQ_USERNAME = 'admin'
	MQ_PASSWD = 'admin123'
	MQ_EXCHANGE = 'bap.today.fanout.exchange'

	BAP_INCREMENT_TODAY = 'bap.data.increment.today.biz'
	BAP_TOCAY_ROUTING_KEY = ''

	tool = rabbitMqTool(MQ_HOST, MQ_PORT, MQ_USERNAME, MQ_PASSWD)
	tool.pushMsg(MQ_EXCHANGE, BAP_TOCAY_ROUTING_KEY, "111")