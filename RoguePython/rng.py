from time import time
from math import sqrt, log

class RNG():
	seed = []

	n = 0
	k0 = 0
	k1 = 0
	k2 = 0
	k3 = 0
	s = []

	def __init__(self):
		self.set_seed()

	def mash(self, data):
		data_str = str(data)

		for i in range(len(data_str)):
			self.n += ord(data_str[i])
			h = 0.02519603282416938 * self.n
			self.n = int(h)
			h -= self.n
			h *= self.n
			self.n = int(h)
			h -= self.n
			self.n += h * 0x100000000

		return int(self.n) * 2.3283064365386963e-10;

	def get_seed(self):
		return self.seed

	def normal(self, mean = 0, std = 1):
		r = 0

		while r > 1 or r == 0:
			u = 2 * self.random() - 1;
			v = 2 * self.random() - 1;
			r = u * u + v * v

		gauss = u * sqrt(-2 * log(r) / r)
		return mean + gauss * std

	def normal_range(self, min, max):
		mean = (min + max) / 2.0
		sigma = (max - mean) / 3.0
		num = min - 1

		while num < min or num > max:
			num = int(self.normal(mean, sigma))

		return num

	def random(self):
		self.k0 = (self.k0 + 1) & 255
		self.k1 = (self.k1 + 1) & 255
		self.k2 = (self.k2 + 1) & 255
		self.k3 = (self.k3 + 1) & 255

		x = self.s[self.k0] - self.s[self.k1]
		if x < 0:
			x += 1

		x -= self.s[self.k2]
		if x < 0:
			x += 1

		x -= self.s[self.k3]
		if x < 0:
			x += 1

		self.s[self.k0] = x
		return x

	def random_range(self, min, max):
		return int(self.random() * (max - min + 1)) + min

	def set_seed(self, *arguments):
		self.s = []
		self.n = 0xefc8249d
		self.k0 = 0
		self.k1 = 58
		self.k2 = 119
		self.k3 = 178

		if len(arguments) == 0:
			args = [time()]
		else:
			args = arguments

		self.seed = []

		for j in range(256):
			self.s.append(self.mash(" "))
			self.s[j] -= self.mash(" ") * 4.76837158203125e-7
			if self.s[j] < 0:
				self.s[j] += 1

		for i in range(len(args)):
			self.seed.append(args[i])

			for j in range(256):
				self.s[j] -= self.mash(args[i])
				self.s[j] -= self.mash(args[i]) * 4.76837158203125e-7
				if self.s[j] < 0:
					self.s[j] += 1
