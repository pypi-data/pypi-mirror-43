import pickle, socket, os, time

#----- CONNECTION SETUP -----#
class connection:
	def __init__(self, port, conn, hostname, os, chunkSize=2):
		self.port = port
		self.conn = conn
		self.hostname = hostname
		self.os = os
		self.chunkSize = chunkSize

	def __str__(self):
		return self.__dict__

#----- SERVER FUNCTIONS -----#
class server():

	def __init__(self):
		print("Server Class Initiated")

	def createSocket(port, chunkSize=2):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(1)

		s.bind(('', int(port)))
		s.listen(1)

		conn, addr = s.accept()

		dataRecieved = globalFuncs.getData(conn, chunkSize)

		os = globalFuncs.recieveData(dataRecieved, "os")
		hostname = globalFuncs.recieveData(dataRecieved, "hostname")
		chunkSize = globalFuncs.recieveData(dataRecieved, "chunkSize")

		return connection(port, conn, hostname, os, chunkSize)

#----- CLIENT FUNCTIONS -----#
class client():

	def __init__(self):
		print("Client Class Initiated")

	def connect(host, port, chunkSize):
		connected = False

		while not connected:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			try:
				s.connect((host, port))

				pcInfo = {}
				pcInfo = globalFuncs.sendData(socket.gethostname(), "hostname", pcInfo)
				pcInfo = globalFuncs.sendData(os.name, "os", pcInfo)
				pcInfo = globalFuncs.sendData(chunkSize, "chunkSize", pcInfo)

				pcInfo = globalFuncs.pushData(s, pcInfo)

				connected = True

			except:
				pass

		#functions.sendData(s, "Computer Name, Comuter OS")
		return s

#----- GLOBAL FUNCTIONS & Vars -----#
class globalFuncs:
	def __init__(self):
		self.loopTime = 1

	def sendData(keyName, data, currentData):
		currentData[keyName] = data
		return currentData

	def pushData(connection, data):
		newData = pickle.dumps(data)
		try:
			connection.send(newData)
			return {}
		except Exception as e:
			return data

	def recieveData(currentData, name):
		return currentData.get(name, "")

	def getData(connection, chunkSize):
		dataRecieved = {}
		while dataRecieved == {}:
			try:
				data = connection.recv(1024 * chunkSize)
				while data == b'':
					data = connection.recv(1024 * chunkSize)
				dataRecieved = pickle.loads(data)
			except Exception as e:
				dataRecieved = {}

		return dataRecieved