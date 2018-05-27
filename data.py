import random as rnd
import math

class data(object):
	# all_solid lungs, colon, stomach, liver, bladder

	nCancers = 6
	cancerName = ["all_solid","lungs", "colon", "stomach", "liver", "bladder"]
	betam = [22., 2.3, 3.2, 4.9, 2.2, 1.2]
	eta = [2.8, 5.2, 2.8, 2.8, 4.1, 6.]      
	gamma = [-4.1, -4,1, -4,1, -4,1, -4,1, -4,1]
	# petDose = [6.23, 3.7, 4.8, 4.1, 4.1, 59.2]
	petDose = [0., 3.7, 4.8, 4.1, 4.1, 59.2]

	# nCancers = 5
	# cancerName = ["lungs", "colon", "stomach", "liver", "bladder"]
	# betam = [2.3, 3.2, 4.9, 2.2, 1.2]
	# eta = [5.2, 2.8, 2.8, 4.1, 6.]      
	# gamma = [-4,1, -4,1, -4,1, -4,1, -4,1]
	# petDose = [3.7, 4.8, 4.1, 4.1, 59.2]

	# delta\\

	L = 5 # Latency

	# petDose = 6.23

	# petDose = [133.1, 3.7, 4.8, 4.1, 4.1, 59.2]

	# petDose = [4.8, 3.7, 4.8, 4.1, 4.1, 59.2]
	# petDose = 

	probDeathCancer = [7., 7., 7., 7., 7.]        # number of people to die from cancer for every type of cancer (per 1000)
	

	probDeath = [0 for i in xrange(0,100)]

	# probDeath =  8.44                          # probability to die just because (n per 1000) 

	nbirth =  12.2                               # number of birth per 1000



	# getters

	def getBetaS(self, sex, i): 
		if sex == 0:
			return self.betam[i]
		else:
			return self.betaf[i]

	def getEta(self, i):
		return self.eta[i]

	def getGamma(self, i):
		return self.gamma[i]

	def getNBirth(self):
		return self.nbirth

	def getProbDeath(self, age):
		return self.probDeath[age-1]
	
	def getProbDeathCancer(self,i):
		return self.probDeathCancer[i]

	def __init__(self, baselineFlag): # baseline flag: 0 - only background, 1 - only PET, 2 - sum

		self.ifBckg = baselineFlag

		self.baselineRisk = [[0 for i in xrange(0, 100)] for j in xrange(0, self.nCancers)]
		self.canProbs = [[] for i in xrange(0, 150)]

		self.readData()
		self.generateProbs()
		# print self.canProbs

	def genBirth(self, n):             # generate a number of kids to born
		nbirth = int(self.getNBirth())              # for example, if it's 3.4/1000 probability:
		dice = rnd.random()                         # it's 0.6 probability to born 3 and 0.4 - to born 4
		if dice < (self.getNBirth() - nbirth):      #
			return int((nbirth + 1.)/1000.*n)        #
		else:
			return int(nbirth/1000.*n)




	def ifDie(self, per):             # check is it time to die     
		dice = rnd.random()
		if per.age <= 96:
			prob = self.getProbDeath(per.age)     # getting probability
		else:
			# prob = self.getProbDeath(96)
			prob = 400.
		if dice < prob/1000.:          # check probability 
			return True
		else:
			return False 



##################################################################
	def generateEAR(self, doseVal, age, aae): # dose, attained age, age at exposure
		ear = []

		if aae < 30 + self.L:   
			eStar = 0
		else:
			eStar = (aae - self.L - 30)/10   

		for iCan in xrange(0, self.nCancers):
			if age < 20:
				ear.append(0)
			else:	
				exponent = math.exp(self.getGamma(iCan) * eStar)
				attainedGuy = ( (age - self.L)/60. )**self.getEta(iCan)
				if self.ifBckg != 0:
					ear.append( self.getBetaS(0, iCan) * doseVal[iCan] * exponent * attainedGuy /10**7 )
				else:
					ear.append(0)
		return ear


	def generateProbs(self):
		for age in xrange(1, 97):
			currentProb = [0 for i in xrange(0, self.nCancers)]
			if self.ifBckg != 1:
				for i in xrange(0, self.nCancers):
					currentProb[i] += self.baselineRisk[i][age-1]

			if age < 25:
				self.canProbs[age] = currentProb
				continue

			for ageAtExposure in xrange(1,age):
				if ageAtExposure > 70:
					break
				currEAR = self.generateEAR(self.petDose, age, ageAtExposure)
				for canType in xrange(0, self.nCancers):
					currentProb[canType] += currEAR[canType]
			self.canProbs[age] = currentProb
		return
########################################################################

	def readData(self):		

		file = []
		file.append(open("data/all_cancers.txt"))
		file.append(open("data/lungs.txt"))
		file.append(open("data/colon.txt"))
		file.append(open("data/stomach.txt"))
		file.append(open("data/liver.txt"))
		file.append(open("data/bladder.txt"))

		for canId in xrange(0,6):
			lines = [line.rstrip('\n') for line in file[canId]]
			words = []
			for k in lines:
				words = k.split(',')
				if words[0] == 'age':
					continue
				self.baselineRisk[canId][int(words[0]) - 1] = float(words[2]) * float(words[3]) / float(words[4])
				if canId == 1:
					self.probDeath[int(words[0]) -1] = float(words[1])*1000.
				words = []
		return

		




		


