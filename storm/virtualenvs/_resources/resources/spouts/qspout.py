# [\0]                                                               #
#                                                                    #
# This code is confidential and proprietary, All rights reserved.    #
#								     #
# Tamar Labs 2015.						     #
#								     #
# @author: Adam Lev-Libfeld (adam@tamarlabs.com)                     #
#								     #

from __future__ import absolute_import, print_function, unicode_literals


from kombu import Connection
from streamparse.spout import Spout
#import common.logger
from common.config import Config


class QSpout(Spout):

	def initialize(self, stormconf, context):
		config = Config()
		self._conn = Connection('librabbitmq://guest:guest@%s:%s//' %
			                (config.queues['host'], config.queues['port']))
		self.queue = self._conn.SimpleQueue(config.queues['intake'])
		#self.logger = common.logger.get_logger(config.queues.intake.name)

	def next_tuple(self):
		message = self.queue.get(block=True)
		try:
			data = message.payload
                        self.emit([0, data])
		except ValueError:
			pass
		except:
			import sys, traceback
			msg = "Unexpected Spout error:%s" % "\n".join(traceback.format_exception(*sys.exc_info()))
			#self.logger.error(msg)
		finally:
			message.ack()
