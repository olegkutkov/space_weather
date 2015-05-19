# -*- coding: UTF-8 -*-
import config

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.ticker
import pylab
import matplotlib.ticker as ticker
import numpy as np
import strings

from ftp_utils import FtpUtil
from date_util import DateUtil
from itertools import islice

from common import *

PLANET_DATA_LABEL = 'Planetary'

def ftp_init():
	dow_ftp = FtpUtil(config.NOAA_FTP_ADDRESS)
	if not dow_ftp.connect() or not dow_ftp.set_auth() or not dow_ftp.chdir(config.NOAA_GEOMAG_DIR):
		print 'Unable to process geomag data!'
		return None

	return dow_ftp

def parse_geomag_lines(lines, skip_first = False):
	data = []

	if lines is None:
		return data

	first_occur = True

	for line in lines:
		if is_comment(line):
			continue

		if PLANET_DATA_LABEL in line:
			splitted = line.split()

			if skip_first and first_occur:
				first_occur = False
				continue

			for k_val in splitted[3:]:
				if k_val != '-1':
					data.append(int(k_val))

	return data

def build_geomag_plot(week_geomag_file, two_days_geomag_file):
	print 'Generating plot...'

	week_file_lines = None
	two_days_geomag_lines = None

	try:
		week_file_lines = open(week_geomag_file).readlines()
		two_days_geomag_lines = open(two_days_geomag_file).readlines()
	except:
		print 'No data for geomag!'
		return None

	week_data = parse_geomag_lines(week_file_lines)
	today_data = parse_geomag_lines(two_days_geomag_lines, True)

	data = week_data + today_data

	y = np.array(data)
	t = np.arange(0, len(data), 1)

	fig, ax1 = plt.subplots()

	plt.xlim(0, len(data))
	plt.ylim(0, 9)

	x_day_labels = []

	for x in range(0, 8):
		dt_util = DateUtil(x)
		x_day_labels.append(dt_util.get_utc_prev_day_ymd_str_pretty())
	
	x_day_labels = x_day_labels[::-1]

	x_formatter = matplotlib.ticker.FixedFormatter(x_day_labels)
	ax1.xaxis.set_major_formatter(x_formatter)

	for tick in ax1.get_xaxis().get_major_ticks():
		tick.set_pad(9.)
		tick.label1 = tick._get_text1()

	plt.plot(t, y, color='g', linewidth=4)
	plt.grid(axis='y', linestyle='-')
	plt.grid(axis='x', linestyle='-')

	plt.xticks(np.arange(0, t[-1] + 1, 7.75))

	plt.xticks(rotation = 90)

	plt.ylabel(u'Kp')

	ax2 = ax1.twinx()
	ax2.set_ylim(0, 9)
	y2_formatter = matplotlib.ticker.FixedFormatter(strings.geomag_y_ticks_right)
	ax2.yaxis.set_major_formatter(y2_formatter)

	plt.title(strings.geomag_plot_title)
	plt.tight_layout()

	out_file = config.FILES_WORK_DIR + '/' + config.GEOMAG_OUT_FILE

	print 'Plot was generated and saved as ' + out_file

	plt.savefig(out_file, dpi = config.PLOT_DPI)

	#plt.show()

	return out_file

def process_geomag_data():
	print '\nWorking - geomag...'

	dow_ftp = ftp_init()

	if dow_ftp is None:
		return

	week_geomag_file = config.GEOMAG_WEEKLY_FILE
	two_days_geomag_file = config.GEOMAG_FILE

	if dow_ftp.download_file(week_geomag_file, config.FILES_WORK_DIR):
		week_geomag_file = config.FILES_WORK_DIR + '/' + week_geomag_file
	else:
		print 'Unable to process geomag data!'
		return

	if dow_ftp.download_file(two_days_geomag_file, config.FILES_WORK_DIR):
		two_days_geomag_file = config.FILES_WORK_DIR + '/' + two_days_geomag_file
	else:
		print 'Unable to process geomag data!'
		return

	dow_ftp.close()

	result_plot_img = build_geomag_plot(week_geomag_file, two_days_geomag_file)

	delete_file(week_geomag_file)
	delete_file(two_days_geomag_file)

	if result_plot_img is None:
		print 'Unable to process geomag data!'
		return

	file_uploader(result_plot_img)

