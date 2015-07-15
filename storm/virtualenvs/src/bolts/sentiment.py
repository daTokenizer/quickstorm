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
from external.text_analyzer import TextAnalyzer

class SentimentDetector(Bolt):
	def initialize(self, storm_conf, context):
                self.text_analyzer = TextAnalyzer()

	def process(self, tup):
                try:
                        message = Message(tup.values[0])
                        rank = self.text_analyzer.calc_sentiment(message.text)
                        message.rank = rank
                        if rank > 0:
                                stream = "pro"
                        else:
                                stream = "con"
                        self.emit([rank , message.serialize()], stream = stream)

		except:
			import sys, traceback
			msg = "Unexpected SentimentBolt (action: %d) error:%s" % (action_num, "\n".join(traceback.format_exception(*sys.exc_info())))
			self.logger.error(msg)
