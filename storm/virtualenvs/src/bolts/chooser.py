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
from external.avatar_ranker import AvatarRanker
from common.data_base_adaptor import DataBaseAdaptor


class Reactor(Bolt):
	def initialize(self, storm_conf, context):
        self.db_adaptor = DataBaseAdaptor()
        self.avatar_ranker = AvatarRanker()
        #TODO: stub

	def process(self, tup):
        try:

            action, message = *tup.values
            avatars = self.db_adaptor.getAvailableAvatars(action)
            ranked_avatars = [(a,self.avatar_ranker.rank(a,action,message)) for a in avatars]
            chosen, max_rank = *(ranked_avatars[0])
            for a,r in ranked_avatars:
                if r > max_rank:
                    chosen = a
                    max_rank = r

            self.emit([chosen, action, message], stream = "assignment")

		except:
			import sys, traceback
			msg = "Unexpected ReactorBolt (action: %d) error:%s" % (action_num, "\n".join(traceback.format_exception(*sys.exc_info())))
			self.logger.error(msg)
