import pickle
from werkzeug.wrappers import Request, Response
from werkzeug.utils import *
import threading
from classes import *
# import traceback

class Controller:
	def __init__(self):
		self.racks = []
		self.rack_lock = threading.Lock()
		self.io_lock = threading.Lock()
		try: 
			f = open('./racks.state','rb')
			self.racks = pickle.loads(f.read())
		except Exception:
			# traceback.print_stack()
			print('failed to read file')
		#TODO read in config/state file
	
	def save_state(self):
		self.io_lock.acquire()
		f = open('./racks.state','wb')
		f.write(pickle.dumps(self.racks))
		f.close()
		self.io_lock.release()
		
	def add_rack(self, **kwargs):
		self.rack_lock.acquire()
		self.racks.append(Rack(kwargs['size']))
		self.rack_lock.release()
		
	#only supports removing the last rack
	def del_rack(self):
		self.racks = self.racks[:-1]
	
	def action_handler(self, request):
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
