import random

class Cookie():
	def __init__(self):
		self.deliciousness = random.randint(100,1000)
		self.exists = True
	def eat(self):
		if self.exists:
			print(f'yum. deliciousness level is {self.deliciousness}')
			self.exists = False
			self.deliciousness = 0
		else:
			print('cookie has already been eaten')
	def __repr__(self):
		if self.exists:
			return ' 🍪 '
		else:
			return 'no cookie :('