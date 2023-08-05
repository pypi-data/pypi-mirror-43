#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""passcrypt module"""

from sys import argv, stdout

from os import path, remove, environ, chmod, stat, makedirs

import socket

from time import time

from yaml import load, dump

from paramiko.ssh_exception import SSHException

from colortext import blu, yel, bgre, tabd, error

from system import userfind, filerotate, setfiletime, filetime

from net.ssh import SecureSHell

from secrecy.gpgtools import GPGTool, GPGSMTool

class PassCrypt(object):
	"""passcrypt main class"""
	dbg = None
	fen = None
	aal = None
	fsy = None
	sho = None
	gsm = None
	gui = None
	chg = None
	try:
		user = userfind()
		home = userfind(user, 'home')
	except FileNotFoundError:
		user = environ['USERNAME']
		home = path.join(environ['HOMEDRIVE'], environ['HOMEPATH'])
	user = user if user else 'root'
	home = home if home else '/root'
	plain = path.join(home, '.pwd.yaml')
	crypt = path.join(home, '.passcrypt')
	timefile = None
	remote = ''
	reuser = user
	recvs = []
	if 'GPGKEYS' in environ.keys():
		recvs = environ['GPGKEYS'].split(' ')
	elif 'GPGKEY' in environ.keys():
		recvs = [environ['GPGKEY']]
	sslcrt = ''
	sslkey = ''
	maxage = 28800
	__weaks = {}
	__oldweaks = {}
	def __init__(self, *args, **kwargs):
		"""passcrypt init function"""
		for arg in args:
			if hasattr(self, arg):
				setattr(self, arg, True)
		for (key, val) in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, val)
		if self.dbg:
			print(bgre(PassCrypt.__mro__))
			print(bgre(tabd(PassCrypt.__dict__, 2)))
			print(' ', bgre(self.__init__))
			print(bgre(tabd(self.__dict__, 4)))
		now = int(time())
		self.msg = '%s %s%s '%(
            blu('enter password for'), yel(self.crypt), blu(':'))
		if self.gui:
			self.msg = 'enter password for %s: '%self.crypt
		kwargs['pwdmsg'] = self.msg
		timefile = self.timefile if self.timefile else \
            path.expanduser('~/.cache/PassCrypt.time')
		if not path.exists(path.dirname(timefile)):
			makedirs(path.dirname(timefile))
		try:
			with open(timefile, 'r') as tfh:
				last = int(tfh.read())
		except (FileNotFoundError, ValueError):
			last = now
			with open(timefile, 'w+') as tfh:
				tfh.write(str(last))
		age = int(now-int(last))
		setattr(self, 'age', age)
		if self.remote and age >= int(self.maxage):
			self._copynews()
		gsks = GPGSMTool().keylist(True)
		if self.gsm or (
              self.gsm is None and self.recvs and [
                  r for r in self.recvs if r in gsks]):
			self.gpg = GPGSMTool(*args, **kwargs)
		else:
			self.gpg = GPGTool(*args, **kwargs)
		self.ssh = SecureSHell(*args, **kwargs)
		__weaks = self._readcrypt()
		try:
			with open(self.plain, 'r') as pfh:
				__newweaks = load(pfh.read())
			if not self.dbg:
				remove(self.plain)
		except FileNotFoundError:
			__newweaks = {}
		if __newweaks:
			setattr(self, 'chg', True)
			__weaks = __weaks if __weaks else {}
			for (su, ups) in __newweaks.items():
				for (usr, pwdcom) in ups.items():
					if su not in __weaks.keys():
						__weaks[su] = {}
					__weaks[su][usr] = pwdcom
		self.__weaks = __weaks

	def __del__(self):
		if self.chg or self.fen or (sorted(set(self.recvs)) != \
		      sorted(set(GPGTool().recvlist(self.crypt)))) or \
              self.fen or self.chg:
			if self._writecrypt(self.__weaks):
				if self.remote and int(self.age) > int(self.maxage):
					if self._copynews():
						print(blu('backed up to remote succesfully'))
				print(blu('encrypted succesfully'))

	def _copynews(self, force=None):
		"""copy new file method"""
		if self.dbg:
			print(bgre(self._copynews))
		try:
			if SecureSHell().scpcompstats(
                  self.crypt, path.basename(self.crypt),
                  remote=self.remote, reuser=self.reuser):
				return True
		except (FileNotFoundError, socket.gaierror, SSHException) as err:
			error(err)
		return False

	def _readcrypt(self):
		"""read crypt file method"""
		if self.dbg:
			print(bgre(self._readcrypt))
		try:
			with open(self.crypt, 'r') as vlt:
				crypt = vlt.read()
		except FileNotFoundError:
			return False
		return load(str(self.gpg.decrypt(crypt)))

	def _writecrypt(self, __weaks):
		"""crypt file writing method"""
		if self.dbg:
			print(bgre(self._writecrypt))
		kwargs = {'output': self.crypt}
		filerotate(self.crypt, 2)
		isok = None
		for _ in range(0, 2):
			isok = self.gpg.encrypt(message=dump(__weaks), **kwargs)
			chmod(self.crypt, 0o600)
			now = int(time())
			setfiletime(self.crypt, (now, now))
			if isok:
				return True

	def adpw(self, usr, pwd=None, com=None):
		"""password adding method"""
		if self.dbg:
			print(bgre(tabd({
                self.adpw: {'user': self.user, 'entry': usr,
                            'pwd': pwd, 'comment': com}})))
		def __askpwdcom(self, sysuser, usr, pwd, com):
			pwd = pwd if pwd else self.gpg.passwd(
                msg='as user %s enter password for entry %s: '%(sysuser, usr))
			if not pwd: return False
			if not com:
				com = input('enter comment (optional): ')
			return [pwd, com]
		if not self.aal:
			if self.user in self.__weaks.keys() and \
                  usr in self.__weaks[self.user].keys():
				return error('entry', usr, 'already exists for user', self.user)
			pwdcom = __askpwdcom(
                self.user, usr, pwd, com)
			if pwdcom:
				self.__weaks[self.user][usr] = pwdcom
			setattr(self, 'chg', True)
		else:
			for u in self.__weaks.keys():
				if usr in self.__weaks[u].keys():
					error('entry', usr, 'already exists for user', u)
					continue
				print('%s:\n  '%u, end='')
				pwdcom = __askpwdcom(
				    u, usr, pwd, com)
				if pwdcom:
					self.__weaks[u][usr] = pwdcom
				setattr(self, 'chg', True)
		return self.__weaks

	def chpw(self, usr, pwd=None, com=None):
		"""change existing password method"""
		if self.dbg:
			print(bgre(tabd({
                self.chpw: {'user': self.user, 'entry': usr, 'pwd': pwd}})))
		def __askpwdcom(sysuser, usr, pwd, com):
			pwd = pwd if pwd else self.gpg.passwd(
                msg='as user %s enter new password for entry %s: '%(
                sysuser, usr))
			if not pwd:
				pwd = self.__weaks[sysuser][usr][0]
			if not com:
				com = input('enter new comment (optional): ')
			if not com and len(self.__weaks[sysuser][usr]) == 2:
				com = self.__weaks[sysuser][usr][1]
			return [pwd, com]
		if not self.aal:
			if self.__weaks and self.user in self.__weaks.keys() and \
                  usr in self.__weaks[self.user].keys():
				self.__weaks[self.user][usr] = __askpwdcom(
                    self.user, usr, pwd, com)
				setattr(self, 'chg', True)
			else:
				error('no entry named', usr, 'for user', self.user)
		else:
			for u in self.__weaks.keys():
				if usr not in self.__weaks[u].keys():
					error('entry', usr, 'does not exist for user', u)
					continue
				print('%s:\n  '%u, end='')
				self.__weaks[u][usr] = __askpwdcom(
                    u, usr, pwd, com)
				setattr(self, 'chg', True)
		return self.__weaks

	def rmpw(self, usr):
		"""remove password method"""
		if self.dbg:
			print(bgre(tabd({self.rmpw: {'user': self.user, 'entry': usr}})))
		if self.aal:
			for u in self.__weaks.keys():
				try:
					del self.__weaks[u][usr]
					setattr(self, 'chg', True)
				except KeyError:
					error('entry', usr, 'not found for', u)
		else:
			try:
				del self.__weaks[self.user][usr]
				setattr(self, 'chg', True)
			except KeyError:
				error('entry', usr, 'not found for', self.user)
		return self.__weaks

	def lspw(self, usr=None, aal=None):
		"""password listing method"""
		if self.dbg:
			print(bgre(tabd({self.lspw: {'user': self.user, 'entry': usr}})))
		aal = True if aal else self.aal
		__ents = {}
		if self.__weaks:
			if aal:
				__ents = self.__weaks
				if usr:
					usrs = [self.user] + \
                        [u for u in self.__weaks.keys() if u != self.user]
					for user in usrs:
						if user in self.__weaks.keys() and \
                              usr in self.__weaks[user].keys():
							__ents = {usr: self.__weaks[user][usr]}
							break
			elif self.user in self.__weaks.keys():
				__ents = self.__weaks[self.user]
				if usr in __ents.keys():
					__ents = {usr: self.__weaks[self.user][usr]}
		return __ents

def lscrypt(usr, dbg=None):
	"""passlist wrapper function"""
	if dbg:
		print(bgre(lscrypt))
	__ents = {}
	if usr:
		__ents = PassCrypt().lspw(usr)
	return __ents




if __name__ == '__main__':
	exit(1)
