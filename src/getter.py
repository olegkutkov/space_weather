#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import config
import date_util
import sys
import os
from datetime import datetime

import proton_flux
import xray
import geomag

if config.PROGRAM_DISABLED:
	sys.exit()

if not os.path.exists(config.FILES_WORK_DIR):
	os.mkdir(config.FILES_WORK_DIR)	

dt_util = date_util.DateUtil()

print '\n *** Session started at ' + dt_util.get_pretty_ymd_str() + ' *** '

proton_flux.process_proton_flux_data()
xray.process_xray_data()
geomag.process_geomag_data()

