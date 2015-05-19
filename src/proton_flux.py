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

def parse_proton_flux_lines(lines):
	data = []

	if lines is not None:
		for line in lines:
			if is_comment(line):
				continue

			splitted_line = line.split()

			if splitted_line[6] != '0':
				continue

			tmp = {}
			tmp[splitted_line[3]] = splitted_line[7]

			data.append(tmp)

	return data

def build_proton_flux_data_lines(curr_file, prev_file, left_hours):
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

	data = parse_proton_flux_lines(curr_file_lines)
	prev_data = {}

	if len(data) == 0 or left_hours != 0:
		prev_data = parse_proton_flux_lines(pref_file_lines)

	return combine_two_data_lists(data, prev_data, left_hours)

def build_proton_flux_graph(curr_file, prev_file, left_hours, dt_util):
	print 'Generating plot...'

	hour_value_pairs = build_proton_flux_data_lines(curr_file, prev_file, left_hours)

	xdata = []
	ydata = []

	x_hour_labels = []

	for hvp in hour_value_pairs:
		xval = hvp.iterkeys().next()

		xval_str = str(xval)

		xdata.append(xval)
		ydata.append(hvp.itervalues().next())

		if xval_str[2:] == '00':
			localized_xval = int(str(xval)[:2]) + int(dt_util.get_local_offset_from_utc())

			if localized_xval > 24:
				localized_xval = localized_xval - 24
			elif localized_xval == 24:
				localized_xval = 0

			x_hour_labels.append(str(localized_xval).zfill(2) + ':00  ')

	fig, ax1 = plt.subplots()

	y = np.array(ydata)
	t = np.arange(0, len(xdata), 1)

	plt.xlim(0, t[-1] + 5.5)

	plt.ylim(0.0, 1.5e+02)

	y_formatter = matplotlib.ticker.FixedFormatter(strings.proton_y_ticks_left)
	ax1.yaxis.set_major_formatter(y_formatter)

	x_formatter = matplotlib.ticker.FixedFormatter(x_hour_labels)
	ax1.xaxis.set_major_formatter(x_formatter)

	plt.plot(t, ydata, color='r', linewidth=2)
	plt.grid(axis='y', linestyle='-')
	plt.grid(axis='x', linestyle='-')
	plt.xticks(np.arange(0, t[-1] + 5.5, 12))
	plt.yticks(np.arange(0, 1.5e+02, 8.0))

	plt.xticks(rotation = config.PLOT_XTICKS_ROTATION)
	plt.ylabel(strings.proton_y_label)

	date_str = dt_util.get_utc_ymd_str_pretty()

	if left_hours != 0:
		date_str = dt_util.get_utc_prev_day_ymd_str_pretty() + ' - ' + date_str

	plt.xlabel(strings.proton_x_labe_part + date_str)

	ax2 = ax1.twinx()
	ax2.set_ylim(-1, 1.5e+01)
	y2_formatter = matplotlib.ticker.FixedFormatter(strings.proton_y_ticks_right)
	ax2.yaxis.set_major_formatter(y2_formatter)

	plt.title(strings.protong_title)
	plt.tight_layout()

	out_file = config.FILES_WORK_DIR + '/' + config.PROTON_FLUX_OUT_FILE

	print 'Plot was generated and saved as ' + out_file
	plt.savefig(out_file, dpi = config.PLOT_DPI)

	#plt.show()

	return out_file

def ftp_init():
	dow_ftp = FtpUtil(config.NOAA_FTP_ADDRESS)
	if not dow_ftp.connect() or not dow_ftp.set_auth() or not dow_ftp.chdir(config.NOAA_ACE_DIR):
		print 'Unable to process proton flux data!'
		return None

	return dow_ftp

def process_proton_flux_data():
	print '\nWorking - proton flux...'

	dow_ftp = ftp_init()

	if dow_ftp is None:
		return

	dt_util = DateUtil()

	proton_flux_curr_file = dt_util.get_utc_ymd_str() + config.PROTON_FLUX_FILE_SUFFIX
	proton_flux_prev_file = dt_util.get_utc_prev_day_ymd_str() + config.PROTON_FLUX_FILE_SUFFIX

	if dow_ftp.download_file(proton_flux_curr_file, config.FILES_WORK_DIR):
		proton_flux_curr_file = config.FILES_WORK_DIR + '/' + proton_flux_curr_file
	else:
		proton_flux_curr_file = ''

	dow_ftp.close()

	left_hours = dt_util.get_left_hours_in_curr_day() - dt_util.get_local_offset_from_utc()

	if left_hours < 0:
		left_hours = 0

	if left_hours > 0:
		dow_ftp = ftp_init()

		if dow_ftp is None:
			return

		if dow_ftp.download_file(proton_flux_prev_file, config.FILES_WORK_DIR):
			proton_flux_prev_file = config.FILES_WORK_DIR + '/' + proton_flux_prev_file
		else:
			proton_flux_prev_file = ''
	else:
		proton_flux_prev_file = ''

	result_plot_img = build_proton_flux_graph(proton_flux_curr_file, proton_flux_prev_file, left_hours, dt_util)

	delete_file(proton_flux_curr_file)
	delete_file(proton_flux_prev_file)

	if result_plot_img is None:
		print 'Unable to process proton flux data!'
		return

	file_uploader(result_plot_img)

