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
import common.config
from external.actions import ActionDB

class Filter(Bolt):
	hotwords = ["fire","red","warm","burn"]
	def initialize(self, storm_conf, context):
                pass

	def process(self, tup):
		try:
                        message = Message(*tup.values[0])
			if self.is_hot(message.text):
				self.emit(message.serialize())
		except:
			import sys, traceback
			msg = "Unexpected FilerBolt (action: %d) error:%s" % (action_num, "\n".join(traceback.format_exception(*sys.exc_info())))
			#self.logger.error(msg)
	
	def is_hot(self,text):
		for word in text:
			if word in hotwords:
				return True
		return False
