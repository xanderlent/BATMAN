import pickle
from werkzeug.wrappers import Request, Response
from werkzeug.utils import *
from classes import *
# import traceback

class Controller:
	def __init__(self):
		self.racks = []
		try: 
			f = open('./racks.state','rb')
			q=f.read()
			print(q)
			self.racks = pickle.loads(q)
		except Exception:
			# traceback.print_stack()
			print('failed to read file')
		#TODO read in config/state file
	
	def save_state(self):
		f = open('./racks.state','wb')
		f.write(pickle.dumps(self.racks))
		f.close()
		
	def add_rack(self, **kwargs):
		self.racks.append(Rack(kwargs['size']))
		
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
