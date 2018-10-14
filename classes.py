class Page:
	def __init__(self, title, href):
		self.href = href
		self.title = title

class Input:
	def __init__(self, label,**kwargs):
		self.label = label 
		self.type = kwargs['type'] if 'type' in kwargs else None
		self.name = kwargs['name'] if 'name' in kwargs else None
		self.value = kwargs['value'] if 'value' in kwargs else None
		self.placeholder = kwargs['placeholder'] if 'placeholder' in kwargs else None
		self.extra = kwargs['extra'] if 'extra' in kwargs else None

class CommandInput(Input):
	def __init__(self, command_name):
		super().__init__('', type='hidden', name='command', value=command_name)

class Action:
	def __init__(self, title, info, *args):
		self.info = info
		self.title = title
		self.inputs = args

class Server:
	def __init__(self, type, size, slot):
		self.type = type
		self.size = size
		self.slot = slot

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

class EmptyServer(Server):
	def __init__(self, slot):
		self.type = 'empty-server'
		self.size = 1
		self.slot = slot

#slots are 0 indexed
class Rack:
	num_racks = 0
	rack_actions = [
		Action('Add Rack', 'Add a rack to the network',
			Input('Size', type='number', name='size', placeholder=42, extra='required'),
			CommandInput('add_rack')),
		Action('Remove Rack', 'Remove the last rack from the network',
			CommandInput('del_rack')),
		]

	def __init__(self, size):
		self.size = size
		self.slots = [EmptyServer(i) for i in range(size)]
		self.id = Rack.num_racks
		Rack.num_racks = Rack.num_racks + 1

	def __del__(self):
		Rack.num_racks = Rack.num_racks - 1

	def add_server(self, server):
		if all(self.slots == EmptyServer(i) for i in range(server.slot, server.slot+server.size)):
			for i in range(server.size - 1):
				self.slots[server.slot + 1 + i] = None
			self.slots[server.slot] = server
			return self.slots[server.slot]
		return None

