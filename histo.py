import matplotlib.pyplot as plt 
import copy as cp

def finish():
	plt.legend()
	plt.show()

class histo(object):

	standardStep = 1.
	screenHistRelation = 40.
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
		self.x = []
		self.y = []
		self.ifNormalize = False
		self.ifRootLike = False
		self.noAutoControl = False
		self.wasHistogramed = False


	def getNEntries(self):
		return self.nEntries


	def setBinContent(self, i, val):
		self.y[i] = val

	def getBinContent(self, i):
		return self.y[i] 

	def appendPoint(self, x, y):
		self.x.append(x)
		self.y.append(y)

	def multiplyByNum(self, n):
		for i in self.y:
			i *= n

	def histAdd(self, h):
		for i in h.data:
			self.data.append(i)

	def clearDivision(self):
		self.underflow = 0
		self.overflow = 0
		self.x = []
		self.y = []


	def fill(self, val):
		self.nEntries += 1.
		self.data.append(val)


	def makeHist(self, normalized = None, rootLike = None):
		if normalized is None:
			normalized = self.ifNormalize
		if rootLike is None:
			rootLike = self.ifRootLike
		if rootLike:
			self.makeRootHist()
		else:
			self.makeRegHist(normalized)



	def makeRegHist(self, normalized = False):
		# self.autodetect()
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
			self.x = x
			self.y = yn
		else:
			self.x = x
			self.y = y
		self.wasHistogramed = True


	def draw(self, normalized = None, rootLike = None, color = 'red', label = ''):
		# self.makeHist(normalized = normalized, rootLike = rootLike)
		return plt.plot(self.x, self.y, color = color, label = label)



	def isAutoDetect(self, cond):
		self.noAutoControl = cond

	def rebin(self,nbins):
		step = (self.xMax - self.xMin)/nbins
		x = [(self.xMin + i*step) for i in xrange(0,nbins)]
		y = [0. for i in x]
		norma = self.nEntries
		data = sorted(self.data)
		for i in data:
			for j in xrange(0,nbins):
				if i >= (x[j] - step/2.) and i <= (x[j] + step/2.):
					y[j] += 1.
		self.x, self.y = []
 		for i in xrange(0, nbins):
			xl =  x[i] - step/2.
			xr =  x[i] + step/2.
			self.appendPoint(xl, y[i])
			self.appendPoint(xr, y[i])


	def generateData(self):
		x = self.x
		y = self.y
		self.nEntries = 0
		for i in y:
			self.nEntries += i
		self.nEntries = int(self.nEntries)
		self.xMax = sorted(x)[0]
		self.xMin = sorted(x)[-1]
		step = x[1]-x[0]
		self.nBins = int( (self.xMax - self.xMin)/step )
		self.data = []
		for i in xrange(0,self.len(y)):
			for j in xrange(0, y[i]):
				self.data.append(x[i])
		self.makeZero()
			


	def autodetect(self):
		data = sorted(self.data)
		xMin = data[0]
		xMax = data[-1]
		relativeStep = (xMax - xMin) / self.screenHistRelation
		if self.xMin is None:
			self.xMin = xMin - relativeStep
		if self.xMax is None:
			self.xMax = xMax + relativeStep

	def makeZero(self):
		# self.data = []
		self.nEntries = len(self.data)
		self.underflow = 0
		self.overflow = 0
		self.x = []
		self.y = []

	def makeRootHist(self):
		# self.clearDivision()
		# self.makeZero()
		# if not self.noAutoControl:
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
				if i >= (x[j] - step/2.) and i <= (x[j] + step/2.):
					y[j] += 1.

		for i in xrange(0, self.nBins):

			xl =  x[i] - step/2.
			xr =  x[i] + step/2.
			self.appendPoint(xl, y[i])
			self.appendPoint(xr, y[i])
			# self.appendPoint(x[i]-step/2., y[i])
			# self.appendPoint(x[i]+step/2., y[i])

		self.wasHistogramed = True



