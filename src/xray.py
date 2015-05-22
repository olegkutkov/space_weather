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

XRAY_MISSING_DATA = '-1.00e+05'

def parse_xray_lines(lines):
	data = []

	if lines is not None:
		for line in lines:
			if is_comment(line):
				continue

			splitted_line = line.split()

			if splitted_line[7] == XRAY_MISSING_DATA:
				continue

			tmp = {}
			tmp[splitted_line[3]] = splitted_line[7]

			data.append(tmp)

	return data

def build_xray_data_lines(curr_file, prev_file, left_hours):
	curr_file_lines = None
	pref_file_lines = None

	try:
		curr_file_lines = open(curr_file).readlines()
	except:
		pass

	try:
		pref_file_lines = open(prev_file).readlines()
	except:
		pass

	if curr_file_lines is None and pref_file_lines is None:
		print 'No data for proton flux!'
		return None

	data = parse_xray_lines(curr_file_lines)
	prev_data = {}

	if len(data) == 0 or left_hours != 0:
		prev_data = parse_xray_lines(pref_file_lines)

	return combine_two_data_lists(data, prev_data, left_hours)


def build_xray_graph(curr_file, prev_file, left_hours, dt_util):
	print 'Generating plot...'

	hour_value_pairs = build_xray_data_lines(curr_file, prev_file, left_hours)	

	xdata = []
	ydata = []

	x_hour_labels = []

	for hvp in hour_value_pairs:
		xval = hvp.iterkeys().next()
		xval_str = str(xval)

		xdata.append(xval)
		ydata.append(hvp.itervalues().next())

		if xval_str[2:] == '00':
			localized_xval = int(str(xval)[:2]) #+ int(dt_util.get_local_offset_from_utc())

			if localized_xval > 24:
				localized_xval = localized_xval - 24
			elif localized_xval == 24:
				localized_xval = 0

			x_hour_labels.append(str(localized_xval).zfill(2) + ':00  ')

	fig, ax1 = plt.subplots()

	y = np.array(ydata)
	t = np.arange(0, len(xdata), 1)

	plt.xlim(0, t[-1] + 5.5)
	plt.ylim(9.9999999999999998e-10, 6.9999999999999998e-06)

	y_formatter = matplotlib.ticker.FixedFormatter(strings.xray_y_ticks_left)
	ax1.yaxis.set_major_formatter(y_formatter)

	plt.plot(t, ydata, color='b', linewidth=2)
	plt.grid(axis='y', linestyle='-')
	plt.grid(axis='x', linestyle='-')

	plt.xticks(rotation = config.PLOT_XTICKS_ROTATION)
	plt.ylabel(u'Вт/м²')

	date_str = dt_util.get_utc_ymd_str_pretty()

	if left_hours != 0:
		date_str = dt_util.get_utc_prev_day_ymd_str_pretty() + ' - ' + date_str

	plt.xlabel(u'\nВремя: ' + date_str + ' UTC+0')

	ax2 = ax1.twinx()
	ax2.set_ylim(9.9999999999999998e-10, 6.9999999999999998e-06)
	y2_formatter = matplotlib.ticker.FixedFormatter(strings.xray_y_ticks_right)
	ax2.yaxis.set_major_formatter(y2_formatter)

	x_formatter = matplotlib.ticker.FixedFormatter(x_hour_labels)
	ax1.xaxis.set_major_formatter(x_formatter)

	for tick in ax1.get_xaxis().get_major_ticks():
		tick.set_pad(12.)
		tick.label1 = tick._get_text1()

        for tick in ax1.get_xticklabels():
                tick.set_rotation(config.PLOT_XTICKS_ROTATION)

	plt.xticks(np.arange(0, t[-1] + 5.5, 12))

	plt.title(strings.xray_plot_tile)
	plt.tight_layout()

	out_file = config.FILES_WORK_DIR + '/' + config.XRAY_OUT_FILE

	print 'Plot was generated and saved as ' + out_file
	plt.savefig(out_file, dpi = config.PLOT_DPI, bbox_inches='tight')

	#plt.show()

	return out_file

def ftp_init():
	dow_ftp = FtpUtil(config.NOAA_FTP_ADDRESS)
	if not dow_ftp.connect() or not dow_ftp.set_auth() or not dow_ftp.chdir(config.NOAA_XRAY_DIR):
		print 'Unable to process xray data!'
		return None

	return dow_ftp

def process_xray_data():
	print '\nWorking - xray...'

	dow_ftp = ftp_init()

	if dow_ftp is None:
		return

	dt_util = DateUtil()

	xray_curr_file = dt_util.get_utc_ymd_str() + config.XRAY_FILE_SUFFIX
	xray_prev_file = dt_util.get_utc_prev_day_ymd_str() + config.XRAY_FILE_SUFFIX

	if dow_ftp.download_file(xray_curr_file, config.FILES_WORK_DIR):
		xray_curr_file = config.FILES_WORK_DIR + '/' + xray_curr_file
	else:
		xray_curr_file = ''

	dow_ftp.close()

	left_hours = dt_util.get_left_hours_in_curr_day() #- dt_util.get_local_offset_from_utc()

	if left_hours < 0:
		left_hours = 0

	if left_hours > 0:
		dow_ftp = ftp_init()

		if dow_ftp is None:
			return

		if dow_ftp.download_file(xray_prev_file, config.FILES_WORK_DIR):
			xray_prev_file = config.FILES_WORK_DIR + '/' + xray_prev_file
		else:
			xray_prev_file = ''
	else:
		xray_prev_file = ''

	result_plot_img = build_xray_graph(xray_curr_file, xray_prev_file, left_hours, dt_util)

	delete_file(xray_curr_file)
	delete_file(xray_prev_file)

	if not result_plot_img:
		print 'Failed to process xray data!'
		return

	file_uploader(result_plot_img)

