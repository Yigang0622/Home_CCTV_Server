# Home_CCTV_Server
# global 
# Created by Yigang Zhou on 2020-01-09.
# Copyright © 2020 Yigang Zhou. All rights reserved.


from cctv import CCTV


class Global(object):

    def __init__(self):
        self.cctv = CCTV()

        print("Global inited")

