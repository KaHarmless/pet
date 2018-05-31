import matplotlib.pyplot as plt 

class histo(object):

	standardStep = 1.
	screenHistRelation = 20.
	missingRatio = 0.1
	nBins = 100


	def __init__(self, nBins = None, xMin = None, xMax = None):
		if nBins is not None:
			self.nBins = nBins
		self.xMin = xMin
		self.xMax = xMax
		self.nEntries = 0
		self.data = []
		self.underflow = 0
		self.overflow = 0


	def fill(self, val):
		self.nEntries += 1.
		self.data.append(val)

	def draw(self, normalized = False, rootLike = False):
		self.autodetect()
		step = (self.xMax - self.xMin)/self.nBins
		x = [(self.xMin + i*step) for i in xrange(0,self.nBins)]
		y = [0. for i in x]
		norma = self.nEntries
		data = sorted(self.data)
		for i in data:
			if i < self.xMin:
				self.underflow += 1.
			if i > self.xMax:
				self.overflow += 1.
			for j in xrange(0,self.nBins):
				if i >= (x[j] - step) and i <= (x[j] + step):
					y[j] += 1.
		if self.underflow > norma * self.missingRatio or self.overflow > norma * self.missingRatio:
			self.xMin = None
			self.xMax = None
			self.autodetect()
		if normalized:
			yn = [i/norma for i in y]
			plt.plot(x,yn)
		else:
			if rootLike:
				xr = []
				yr = []
				for i in xrange(0,self.nBins):
					xr.append(x[i])
					yr.append(y[i])
					if i == self.nBins - 1:
						break
					if y[i+1] > y[i]:
						xr.append(x[i+1])
						yr.append(y[i])
					elif y[i+1] < y[i]:
						xr.append(x[i])
						yr.append(y[i+1])
				plt.plot(xr,yr)
			else:
				plt.plot(x,y)
		plt.show()


	def autodetect(self):
		data = sorted(self.data)
		xMin = data[0]
		xMax = data[-1]
		# nBins = int((xMax - xMin) / self.standardStep)
		relativeStep = (xMax - xMin) / self.screenHistRelation

		if self.xMin is None:
			self.xMin = xMin - relativeStep
		if self.xMax is None:
			self.xMax = xMax + relativeStep
		# if self.nBins is None:
		# 	self.nBins =  
		












