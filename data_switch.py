from random import choice
import json

import cherrypy

import os
current_dir = os.path.dirname(os.path.abspath(__file__))

class Signals():

    rooms = {}

    def clear(self):
        self.rooms = {}
        return json.dumps({ 'keys': [x for x in self.rooms.keys()] })
    clear.exposed = True

    def list(self):
        return json.dumps([x for x in self.rooms.keys() if ':offer' in x])
    list.exposed = True

    @cherrypy.tools.json_in()
    def get(self):
        result = self.rooms.get(
            cherrypy.request.json['id'],
            None
        );

        if result is None:
            raise cherrypy.HTTPError(404)
        return json.dumps(result);
    get.exposed = True

    @cherrypy.tools.json_in()
    def set(self):
        data = cherrypy.request.json

        self.rooms[data['id']] = data['data']
        print('SET:{0}={1}'.format(
            data['id'],
            data['data']
        ))
        return json.dumps({ 'status': 'OK' })
    set.exposed = True

    def default(self):
        return cherrypy.lib.static.serve_file(
            os.path.join(current_dir, 'index.html')
        )
    default.exposed = True

cherrypy.quickstart(
    root=Signals(),
    config={
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8003
        },
        '/': {
            'tools.staticdir.root': os.getcwd(),
        },
        '/signal': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'signal'
        }
    })