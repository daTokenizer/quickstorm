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
from common.data_base_adaptor import DataBaseAdaptor

class DBLoader(Bolt):
	def initialize(self, storm_conf, context):
                self.db_adaptor = DataBaseAdaptor()
                #TODO: stub

	def process(self, tup):
                try:
			if (tup.stream == "pro"):
                                self.db_adaptor.postPositive(*tup.values)
			elif (tup.stream == "con"):
                                self.db_adaptor.postNegative(*tup.values)
			else:
				self.logger.log("ERROR: got bad tuple")
		except:
			import sys, traceback
			msg = "Unexpected DBLoader (action: %d) error:%s" % (action_num, "\n".join(traceback.format_exception(*sys.exc_info())))
			self.logger.error(msg)
