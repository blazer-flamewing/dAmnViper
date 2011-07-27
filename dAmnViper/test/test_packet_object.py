''' dAmnViper.test.test_packet_object module
    Created by photofroggy
    
    This module provides unit tests for testing the packet parser object found
    in dAmnViper.parse.
'''

from twisted.trial import unittest

from dAmnViper.parse import Packet

class TestPacketObject(unittest.TestCase):
    """ Unit tests for the packet parser. """
    
    def test_simple_packet(self):
        """ Test parsing a simple packet. """
        packet = Packet('command parameter\nargument=value\n\nbody')
        
        self.failIf(packet.cmd != 'command',
            'Parser did not correctly recognise the packet command')
        
        self.failIf(packet.param != 'parameter',
            'Parser did not correctly recognise the packet parameter')
        
        self.failIf(packet.args != {'argument': 'value'},
            'Parser did not interpret packet arguments properly')
        
        self.failIf(packet.body != 'body',
            'Parser did not store the correct packet body')
    
    def test_broken_arguments(self):
        """ Test parsing packets with broken arguments. """
        packet = Packet('command parameter\nargument=\n\nbody')
        
        self.failIf(packet.args != {'argument': ''},
            'Parser stored an incorrect value for the broken argument')
        
        self.failIf(packet.body != 'body',
            'Parser did not store the correct packet body')

# EOF
