#! /usr/bin/env python3
from sys import maxsize as sys_maxsize
from hashlib import new as hash_new
from hashlib import algorithms_available

from .file_op import BasicFileOp, ProgressBar
from .printing import print_msg
from .exception import *


class HashOp(BasicFileOp):
	HASH_TYPE = algorithms_available

	def __init__(self, src, hash_type, digest_size):
		super().__init__(src, 'hash')
		self.hash_type = hash_type.lower()
		self.digest_size = digest_size
		if not self.is_file:
			raise FileNotFound(self.name_src)
		if not self.is_readable:
			raise ReadAccessError(self.name_src)
		# Alias pour blake: choix auto en fonction de l'architecture
		if self.hash_type == 'blake':
			is_64bits = sys_maxsize > 2**32
			if is_64bits:
				self.hash_type = 'blake2b'
			else:
				self.hash_type = 'blake2s'
		if not self.hash_type in self.HASH_TYPE:
			raise HashTypeUnavailable(self.hash_type)
		if self.digest_size <= 0:
			self.digest_size = 1 
		# Vérifier cohérence hash-type -> digest-size
		if self.hash_type == 'blake2b' and self.digest_size > 32:
			self.digest_size = 32
		if self.hash_type == 'blake2s' and self.digest_size > 16:
			self.digest_size = 16

	def launch(self):
		read = 0
		hash_src = ''
		hash_func = hash_new(
			self.hash_type, 
			digest_size=self.digest_size)
		progress_bar = ProgressBar(
			self.filename, 
			self.size, 
			self.op_name)
		try:
			if self.size > 0:
				# Gestion affichage progression
				with progress_bar as pbar:
					for block in self.read_bytes(self.src):
						hash_func.update(block)
						read += len(block)
						pbar.display(read)
			# Prise en compte cas special pour shake (voir doc python)
			if self.hash_type.startswith('shake'):
				hash_src = hash_func.hexdigest(self.digest_size)
			else:
				hash_src = hash_func.hexdigest()
			print_msg(self.hash_type, hash_src)
		except KeyboardInterrupt:
			raise OperationAbort(self.op_name)
		return hash_src
