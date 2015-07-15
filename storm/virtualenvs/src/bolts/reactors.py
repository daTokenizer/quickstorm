# [\0]                                                               #
#                                                                    #
# This code is confidential and proprietary, All rights reserved.    #
#								     #
# Tamar Labs 2015.						     #
#								     #
# @author: Adam Lev-Libfeld (adam@tamarlabs.com)                     #
#								     #

from __future__ import absolute_import, print_function, unicode_literals


from streamparse.bolt import Bolt
import common.logger
from external.reactors.simple import Pro as ProReactor
from external.reactors.simple import Con as ConReactor

class Reactor(Bolt):
	def initialize(self, storm_conf, context):
                self.pro_reactor = ProReactor()
                self.con_reactor = ConReactor()
                #TODO: stub

	def process(self, tup):
        try:
            message = tup.values[1]
			if (tup.stream == "pro"):
                action = self.pro_reactor.react(*tup.values)
			elif (tup.stream == "con"):
                action = self.con_reactor.react(*tup.values)
			else:
                self.logger.log("ERROR: got bad tuple")
                pass
            self.emit([action,message], stream = "reaction")
		except:
			import sys, traceback
			msg = "Unexpected ReactorBolt (action: %d) error:%s" % (action_num, "\n".join(traceback.format_exception(*sys.exc_info())))
			self.logger.error(msg)
