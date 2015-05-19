#!/usr/bin/env python

# -*- coding: utf-8 -*-

import ftplib, socket, os

class FtpUtil:
	def __init__(self, srv_addr):
		self.srv_addr_ = srv_addr
		self.ftp_conn_ = None

	def connect(self):
		try:
			print 'Connecting to ' + self.srv_addr_
			self.ftp_conn_ = ftplib.FTP(self.srv_addr_, timeout=10)
		except (socket.error, socket.gaierror), e:
			print 'Failed to connect to ' + self.srv_addr_ + ' error: ' + str(e)
			return False

		return True

	def close(self):
		self.ftp_conn_.quit()

	def set_auth(self, login = 'anonymous', passwd = ''):
		try:
			self.ftp_conn_.login(login, passwd)
		except ftplib.error_perm:
			print 'Login as ' + login + ' failed!'
			self.close()
			return False

		return True

	def chdir(self, path):
		try:
			self.ftp_conn_.cwd(path)
		except ftplib.error_perm:
			print 'Failed to change directory to ' + path
			self.close()
			return False

		return True

	def download_file(self, file_name, save_dir):
		try:
			print 'Downloading ' + file_name + ' to ' + save_dir
			self.ftp_conn_.retrbinary('RETR %s' % file_name, open(save_dir + '/' + file_name, 'w').write)
		except Exception, e:
			print 'Failed to read file ' + file_name
			return False

		return True

	def upload_file(self, full_file_name):
		file_ext = os.path.splitext(full_file_name)[1]
		file_name = os.path.split(full_file_name)[1]

		print 'Uploading ' + file_name

		try:
			if file_ext in (".txt", ".htm", ".html"):
				self.ftp_conn_.storlines("STOR " + file_name, open(full_file_name))
			else:
				self.ftp_conn_.storbinary("STOR " + file_name, open(full_file_name, "rb"), 1024)
		except Exception, e:
			print 'Upload failed ' + str(e)
			return False

		return True


