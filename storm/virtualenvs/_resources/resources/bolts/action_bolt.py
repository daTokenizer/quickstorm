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
#import common.logger
from external.actions import ActionDB

class ActionBolt(Bolt):
	def initialize(self, storm_conf, context):
                actionDB = ActionDB()

	def process(self, tup):
		try:
                        action_num = tup.values[0]
                        if action_num < len(actionDB.actions):
                                data = actionDB.actions[action_num](tup.values[1])
                                self.emit([action_num+1 , data], stream = "next_action")
                        else:
                                self.emit([data], stream = "output_to_queue")
		except:
			import sys, traceback
			msg = "Unexpected ActionBolt (action: %d) error:%s" % (action_num, "\n".join(traceback.format_exception(*sys.exc_info())))
			#self.logger.error(msg)
