# -*- coding: UTF-8 -*-

import os
import config
from ftp_utils import FtpUtil

def is_comment(line):
	return '#' in line or ':' in line

def combine_two_data_lists(data, prev_data, left_hours):
	if len(data) == 0:
		return prev_data

	prev_end = []

	for val in prev_data:
		hour = int(val.iterkeys().next()[:2])

		if (24 - hour) <= left_hours:
			prev_end.append(val)

	return prev_end + data

def delete_file(full_file_name):
	try:
		os.remove(full_file_name)
	except Exception, e:
		print 'Failed to remove ' + full_file_name + ' ' + str(e)
		pass

def file_uploader(full_fule_name):
	up_ftp = FtpUtil(config.UPLOAD_FTP_ADDRESS)

	if not up_ftp.connect() or not up_ftp.set_auth(config.UPLOAD_FTP_LOGIN, config.UPLOAD_FTP_PASSWORD) or not up_ftp.chdir(config.UPLOAD_FTP_DIR):
		print 'Unable to process proton flux data!'
		return

	up_ftp.upload_file(full_fule_name)

