# A simple key/value store webserver.

import os
import json
from random import choice

import cherrypy


class Signals():

    data = {}

    # Get a value.
    @cherrypy.tools.json_in()
    def get(self):
        result = self.data.get(
            cherrypy.request.json['id'],
            None
        );

        if result is None:
            raise cherrypy.HTTPError(404)

        return json.dumps(result);
    get.exposed = True

    # Set a value
    @cherrypy.tools.json_in()
    def set(self):
        data = cherrypy.request.json

        self.data[data['id']] = data['data']
        print('SET:{0}={1}'.format(
            data['id'],
            data['data']
        ))
        return json.dumps({ 'status': 'OK' })
    set.exposed = True

    #By default serve index.html in the cwd
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
