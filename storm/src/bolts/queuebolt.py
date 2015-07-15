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
from common.config import Config

class QBolt(Bolt):
	def initialize(self, storm_conf, context):
                config = Config()
                self._conn = Connection('librabbitmq://guest:guest@%s:%s//' %
			                (config.queues['host'], config.queues['port']))
		self.queue = self._conn.SimpleQueue(config.queues['output'])
		#self.logger = common.logger.get_logger(config.queues.output.name)

	def process(self, tup):
		try:
                        data = tup.values[0]
                        self.queue.put(data)
		except:
			import sys, traceback
			msg = "Unexpected QBolt error:%s" % "\n".join(traceback.format_exception(*sys.exc_info()))
			#self.logger.error(msg)
