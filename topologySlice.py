'''
Coursera:
- Software Defined Networking (SDN) course
-- Network Virtualization

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
from collections import defaultdict

import pox.openflow.libopenflow_01 as of
import pox.openflow.discovery
import pox.openflow.spanning_tree

from pox.lib.revent import *
from pox.lib.util import dpid_to_str
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
from collections import namedtuple
import os

log = core.getLogger()


class TopologySlice (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Slicing Module")
        
        
    """This event will be raised each time a switch will connect to the controller"""
    def _handle_ConnectionUp(self, event):
        
        # Use dpid to differentiate between switches (datapath-id)
        # Each switch has its own flow table. As we'll see in this 
        # example we need to write different rules in different tables.
        dpid = dpidToStr(event.dpid)
        log.debug("Switch %s has come up.", dpid)

        """ Add your logic here """
	#methodList = [method for method in dir(event)]
	#log.debug(str(methodList))
	ftMap = {"01":[(3,1), (4,2)], "02":[(1,2)], "03":[(1,2)], "04":[(1,3), (2,4)]}
	connection = event.connection
	switch = dpid.split("-")[-1]
	if switch in ftMap:
	    portPairLs = ftMap[switch]
	    for portPair in portPairLs:
	    	connection.send( of.ofp_flow_mod( action=of.ofp_action_output( port=portPair[0] ),
                                       		  match=of.ofp_match(in_port=portPair[1])))
	    	connection.send( of.ofp_flow_mod( action=of.ofp_action_output( port=portPair[1] ),
                                       		  match=of.ofp_match(in_port=portPair[0])))


        

def launch():
    # Run spanning tree so that we can deal with topologies with loops
    pox.openflow.discovery.launch()
    pox.openflow.spanning_tree.launch()

    '''
    Starting the Topology Slicing module
    '''
    core.registerNew(TopologySlice)
