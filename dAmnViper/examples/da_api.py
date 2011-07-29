''' Example usage of deviantart API objects.
    Created by photofroggy.
'''

import os
import sys
from twisted.internet import reactor

sys.path.insert(0, os.curdir)

from dAmnViper.dA import api


class MyApplication(object):
    """ Just an example type thingy. """
    
    def __init__(self, _reactor, id, secret, port=8080, agent='dAmnViper/example/daapiclient', state=None):
        self.id = id
        self.secret = secret
        self.port = port
        self.state = state
        # Set up the API client
        self.api = api.APIClient(_reactor, id, secret, agent=agent)
    
    def start(self, redirect):
        """ Start the application.
            
            All this really does is start the auth server and then display a
            url on screen. The user should visit this url to authorize the app.
        """
        d = self.api.auth_app(self.port)
        d.addCallbacks(self.authSuccess, self.authFailure)
        # Make a url
        url = self.api.url('authorize',
            client_id=self.id,
            client_secret=self.secret,
            redirect_uri=redirect,
            response_type='code',
            state=self.state
        )
        # Send user there, somehow...
        sys.stdout.write('>> Visit the following URL to authorize this app:\n')
        sys.stdout.write('>> {0}\n'.format(url))
        
        # Now we wait for the user's webbrowser to be redirected to our server.
    
    def authSuccess(self, response):
        """ Called when the app is successfully authorized. """
        sys.stdout.write('>> Got auth code!\n')
        sys.stdout.write('>> Requesting access token...\n')
        d = self.api.grant(req_state=self.state)
        d.addCallback(self.grantSuccess, self.grantFailure)
    
    def authFailure(self, response):
        """ Called when authorization fails. """
        sys.stdout.write('>> Authorization failed.\n')
        sys.stdout.write('>> Printing debug data...\n')
        sys.stdout.write('>> {0}\n'.format(response.args))
    
    def grantSuccess(self, response):
        """ Called when the app is granted access to the API. """
        sys.stdout.write('>> Got an access token!\n')
        sys.stdout.write('>> Getting user information...\n')
        # whoami?
        self.api.user_whoami().addCallback(self.whoami)
        # damntoken?
        self.api.user_damntoken().addCallback(self.damntoken)
    
    def grantFailure(self, response):
        """ Called when the app is refused access to the API. """
        sys.stdout.write('>> Failed to get an access token.\n')
        sys.stdout.write('>> Printing debug data...\n')
        sys.stdout.write('>> {0}\n'.format(response.data))
    
    def whoami(self, response):
        """ Handle the response to whoami API call. """
        if not 'username' in response.data:
            sys.stdout.write('>> whoami failed.\n')
            return
        
        sys.stdout.write('>> Account: {0}{1}\n'.format(
            response.data['symbol'], response.data['username']))
    
    def damntoken(self, response):
        """ Handle the response to whoami API call. """
        if response.data is None:
            sys.stdout.write('>> damntoken failed.\n')
            return
        
        sys.stdout.write('>> Authtoken: {0}\n'.format(response.data))


if __name__ == '__main__':
    
    app = MyApplication(reactor,
        'my_client_id',
        'my_client_secret'
    )
    
    app.start('http://localhost:8080')


# EOF
