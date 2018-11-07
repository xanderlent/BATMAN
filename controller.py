import pickle, json, re
from werkzeug.wrappers import Request, Response
from werkzeug.utils import *
import threading, logging
from classes import *
from io import StringIO
# import traceback

class Controller:
	def __init__(self):
		self.templates = []
		self.log_stream = StringIO()
		self.log = logging.getLogger('batman')
		self.log.setLevel(logging.DEBUG)
		self.log.addHandler(logging.StreamHandler(stream=self.log_stream))
		self.log.addHandler(logging.FileHandler('batman.log'))
		self.log.info('starting controller')
		self.racks = []
		self.rack_lock = threading.Lock()
		self.io_lock = threading.Lock()
		try: 
			f = open('./racks.state','rb')
			self.racks = pickle.loads(f.read())
		except Exception:
			self.log.warning('Failed to load rack state')
			
		#TODO read in config/state file
	def get_log(self, lines):
		print(self.log_stream.getvalue())
		print('\n'.join(self.log_stream.getvalue().split('\n')[-lines:]))
		return '\n'.join(self.log_stream.getvalue().split('\n')[-lines:])
		
	def save_state(self):
		self.io_lock.acquire()
		f = open('./racks.state','wb')
		f.write(pickle.dumps(self.racks))
		f.close()
		self.io_lock.release()
		
	def add_rack(self, **kwargs):
		if kwargs['size'] <= 0 :
			return
		self.rack_lock.acquire()
		self.racks.append(Rack(kwargs['size']))
		self.log.info("added rack #%d" % (len(self.racks)-1))
		self.rack_lock.release()
		
	#only supports removing the last rack
	def del_rack(self):
		self.rack_lock.acquire()
		self.racks = self.racks[:-1]
		self.log.info("removed rack #%d" % len(self.racks))
		self.rack_lock.release()
		
		
	def add_server(self, **kwargs):
		self.rack_lock.acquire()
		self.racks[kwargs['rack']].add_server(Server(kwargs['size'],kwargs['slot'],kwargs['rack'],kwargs['hostname']))
		self.log.info("adding server")
		self.rack_lock.release()
		
		
	def rack_action_handler(self, request):
		if 'command' not in request.form:
			return Response("Error malformed request")
		params = {}
		for a in Rack.rack_actions:
			if request.form['command'] == a.inputs[-1].value:
				for i in a.inputs[:-1]:
					if i.name not in request.form:
						return Response("Error, malformed " + request.form['command'] +" command")
					if i.type.lower() in ['number']:
						params[i.name] = int(request.form[i.name], 10)
					else:
						params[i.name] = request.form[i.name]
				getattr(self, request.form['command'])(**params)
				self.save_state()
				if request.referrer is None:
					return redirect('/')
				return redirect(request.referrer)

	def get_server_details(self, request):
		# print('getting details')
		result = {}
		if 'rack' not in request.args:
			  result = {'err':'no rack arg'}
			  return result
		if 'server' not in request.args:
			  result = {'err':'no server arg'}
			  return result
		try:
			r = int(request.args['rack'], 10)
			s = int(request.args['server'], 10)
		except Exception as ex:
			result = {'err': 'error converting to int'}
			return result
		# print(r,s)
		print('returning details')
		result = self.racks[r].slots[s]
		return json.dumps(result.__dict__)
		