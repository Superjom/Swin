# -*- coding: utf-8 -*-
import sys
reload(sys)

from communitor import *

dt = DataTransfer()
dt.sendHaltSignal()
dt.sendInitSignal()
dt.sendResumeSignal()
