#!/usr/bin/env python3
import os
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader

from classes import *
from controller import *

class Batman(object):

	def __init__(self):
		#set up jinja
		template_path = os.path.join(os.path.dirname(__file__), 'templates')
		self.jinja_env = Environment(loader=FileSystemLoader(template_path),autoescape=True, trim_blocks=True, lstrip_blocks=True)
		#define endpoints
		self.url_map = Map([
			Rule('/', endpoint='rack'),
			Rule('/rack', endpoint='rack'),
			Rule('/rackdetail', endpoint='rack'),
			Rule('/rackup', endpoint='rackup'),
			Rule('/network', endpoint='network'),
			Rule('/switch', endpoint='switch'),
			Rule('/action', endpoint='action'),
		])
		#list of pages for navigation
		self.navpages = [
			Page('Racks','/rack'),
			Page('Network','/network'),
			Page('Media','/media'),
			]
		self.controller = Controller()

	def	dispatch_request(self, request):
		adapter = self.url_map.bind_to_environ(request.environ)
		try:
			endpoint, values = adapter.match()
			return getattr(self, 'on_' + endpoint)(request, **values)
		except HTTPException as e:
			return e

	def	wsgi_app(self, environ, start_response):
		request = Request(environ)
		response = self.dispatch_request(request)
		return response(environ, start_response)

	def	__call__(self, environ, start_response):
		return self.wsgi_app(environ, start_response)

	def render_template(self, template_name, **context):
		t = self.jinja_env.get_template(template_name)
		return Response(t.render(context), mimetype='text/html')

	def on_rack(self, request):
		print(self.controller.racks)
		return self.render_template('rack.html',
			pages=self.navpages,
			actions=Rack.rack_actions,
			racks=self.controller.racks)

	def on_action(self, request):
		return self.controller.action_handler(request)
	


def create_app(with_static=True):
	app = Batman()
	if with_static:
		app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
		'/static':  os.path.join(os.path.dirname(__file__), 'static')
		})
	return app


	
if __name__ == '__main__':
	from werkzeug.serving import run_simple
	app = create_app()
	run_simple('0.0.0.0', 8084, app, use_debugger=True, use_reloader=True)
