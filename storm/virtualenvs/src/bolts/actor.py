# [\0]                                                               #
#                                                                    #
# This code is confidential and proprietary, All rights reserved.    #
#								     #
# Tamar Labs 2015.						     #
#								     #
# @author: Adam Lev-Libfeld (adam@tamarlabs.com)                     #
#								     #

from __future__ import absolute_import, print_function, unicode_literals


from kombu import simple, Connection
from streamparse.bolt import Bolt
import common.logger
from external.simple_actor import Actor

class ActorBolt(Bolt):
	def initialize(self, storm_conf, context):
        self.actor = Actor()

	def process(self, tup):
		try:
			if (tup.stream == "assignment"):
                self.actor.perform(*tup.values)
			else:
                self.logger.log("ERROR: got bad tuple")
		except:
			import sys, traceback
			msg = "Unexpected ActorBolt (action: %d) error:%s" % (action_num, "\n".join(traceback.format_exception(*sys.exc_info())))
			self.logger.error(msg)
