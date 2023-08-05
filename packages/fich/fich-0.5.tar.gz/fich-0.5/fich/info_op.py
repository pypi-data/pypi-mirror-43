#! /usr/bin/env python3
from stat import filemode as stat_filemode
from datetime import datetime

from .file_op import BasicFileOp
from .printing import print_msg
from .exception import *


class InfoOp(BasicFileOp):
	def __init__(self, src):
		super().__init__(src, 'info')
		if not self.is_file:
			raise FileNotFound(self.name_src)

	def get_owner(self, uid):
		res = '?'
		try:
			# Disponible sur Linux
			from pwd import getpwuid as pwd_getpwuid
			res = pwd_getpwuid(uid)[0]
		except ImportError:
			pass
		return res

	def get_group(self, gid):
		res = '?'
		try:
			# Disponible sur Linux
			from grp import getgrgid as grp_getgrgid
			res = grp_getgrgid(gid)[0]
		except ImportError:
			pass
		return res

	def get_last_access(self, timestamp):
		res = ''
		now = datetime.today()
		last_access = datetime.fromtimestamp(timestamp)
		if now.date() == last_access.date():
			res = last_access.strftime('%H:%M')
		else:
			res = last_access.strftime('%d-%m-%Y %H:%M')
		return res

	def get_size_repr(self, size):
		res = ''
		if size <= 1024:
			res = '{}'.format(size)
		elif size <= 1024 ** 2:
			res = '{0:.2f} Ko'.format(size/1024)
		elif size <= 1024 ** 3:
			res = '{0:.2f} Mo'.format(size/(1024**2))
		else:
			res = '{0:.2f} Go'.format(size/(1024**3))
		return res

	def launch(self):
		try:
			info = stat_filemode(self.info.st_mode) + ' '
			info += '{} '.format(self.info.st_nlink)
			info += self.get_owner(self.info.st_uid) + ' '
			info += self.get_group(self.info.st_gid) + ' '
			info += self.get_size_repr(self.size) + ' '
			info += self.get_last_access(self.info.st_atime) + ' '
			info += '{}'.format(self.info.st_ino)
			print_msg(self.op_name, info)
		except KeyboardInterrupt:
			raise OperationAbort(self.op_name)
		return info
