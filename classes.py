from enum import Enum

class Interface:
	def __init__(self, name, server):
		self.server = server
		self.name = name

class Vlan:
	def __init__(self, vlan_id, name='',description=''):
		self.vlan_id = vlan_id
		self.name = name
		self.description = description

class PortMode(Enum):
	ACCESS = 1
	TRUNK = 2

class Connection:
	def __init__(self, server_int, switch_int, port_mode):
		self.server_int = server_int
		self.switch_int = switch_int
		self.port_mode = port_mode
		self.vlans = []
	
	def add_vlan(self, vlan):
		self.vlans += vlan
		
	def del_vlan(self, vlan):
		del(self.vlans[self.vlans.index(vlan)])


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
	def __init__(self, size, slot, rack, hostname, type = 'default-server'):
		self.type = type
		self.size = size
		self.slot = slot
		self.hostname = hostname
		self.rack = rack
		self.interfaces = []
		#todo check if hostname in foreman database
		self.managed = False
	
	def add_interface(interface):
		self.interfaces += interface

	def del_interface(interface):
		del(self.interfaces[self.interfaces.index(interface)])
		
	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

class EmptyServer(Server):
	def __init__(self, slot, rack):
		super().__init__(1, slot, rack, '', 'empty-server')

#slots are 0 indexed
class Rack:
	num_racks = 0
	rack_actions = [
		Action('Add Rack', 'Add a rack to the network',
			Input('Size', type='number', name='size', placeholder=42, extra='required'),
			CommandInput('add_rack')),
		Action('Remove Rack', 'Remove the last rack from the network',
			CommandInput('del_rack')),
		Action('Add Server', 'Add a server to a rack',
			Input('Rack #', type='number', name='rack'),
			Input('Slot #', type='number', name='slot'),
			Input('Size',   type='number', name='size'),
			Input('Hostname', type='text', name='hostname'),
			CommandInput('add_server')),
		]

	def __init__(self, size):
		self.size = size
		self.id = Rack.num_racks
		self.slots = [EmptyServer(i, self.id) for i in range(size)]
		Rack.num_racks = Rack.num_racks + 1

	def __del__(self):
		Rack.num_racks = Rack.num_racks - 1

	def add_server(self, server):
		if all(self.slots[i] == EmptyServer(i, self.id) for i in range(server.slot, server.slot+server.size)):
			for i in range(server.size - 1):
				self.slots[server.slot + 1 + i] = None
			self.slots[server.slot] = server
			return self.slots[server.slot]
		return None

