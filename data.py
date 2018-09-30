import random as rnd
import math
import histo as h
import person as p
import copy as cp 

class data(object):


	# all_solid lungs, colon, stomach, liver, bladder

	expDur = 100
	nPeople = 10**6

	maxPetAge = 80
	minPetAge = 20

	
	nCancers = 6
	cancerName = ["all_solid","lungs", "colon", "stomach", "liver", "bladder"]
	betam = [22., 2.3, 3.2, 4.9, 2.2, 1.2]
	eta = [2.8, 5.2, 2.8, 2.8, 4.1, 6.]      
	gamma = [-4.1, -4,1, -4,1, -4,1, -4,1, -4,1]
	# petDose = [6.23, 3.7, 4.8, 4.1, 4.1, 59.2]
	petDose = [0., 3.7, 4.8, 4.1, 4.1, 59.2]

	nStages = [3 for i in xrange(0,nCancers)]

	agesUnderRad = [0 for i in xrange(0, 200)]


	probDetect = 	  [ [ 0.,  0.,  0. ],   # all_solid 
	                    [96., 88. , 94.],   # lungs, 
	                    [95., 29.,  78.],   # colon, 
	                    [47., 34. , 50.],   # stomach,
	                    [82., 63.,  21.],   # liver, 
	                    [60., 85., 100.] ]  # bladder
	      


	# one year survival rate
	# probSurv =        [ [100.,  100.,   100.],    # all_solid  
	#                     [80.22, 62.55, 25.09],    # lungs, 
	#                     [95.72, 91.47, 56.84],    # colon, 
	#                     [81.46 , 70.25, 29.16],   # stomach,
	#                     [66.56,  37.59, 15.35],   # liver, 
	#                     [89.20,  71.17, 29.81] ]  # bladder

	# five years survival
	probSurv =        [ [100.,  100.,   100.],    # all_solid  
	                    [56.3, 29.7, 4.7],    # lungs, 
	                    [89.8, 72.1, 13.8],    # colon, 
	                    [68.1, 30.6, 5.2],   # stomach,
	                    [31.3,  10.6, 2.4],   # liver, 
	                    [69.4,  34.9, 4.8] ]  # bladder



	L = 5 # Latency

	ageDistrib = dict()
	ageDistribFull = dict()


	probDeath = [0 for i in xrange(0,100)]
	# nbirth =  12.5 * 0.51		  # 51% of born are males 
	nbirth = 0

	                              # number of birth per 1000

	def __init__(self,baselineFlag, period = 1): # baseline flag: 0 - only background, 1 - all together!!!!!!!!!
		self.period = period
		self.initAgesAtPET()

		self.ifBckg = baselineFlag

		self.baselineRisk = [[0 for i in xrange(0, 100)] for j in xrange(0, self.nCancers+1)]
		self.canProbs = [[[] for age in xrange(0, 150)] for start in xrange(0,150)]

		self.initialCan = [[0 for i in xrange(0, self.nCancers+1)] for j in xrange(0, 100)]

		self.canStage =[[h.histo(self.expDur, -0.5, self.expDur-0.5) for j in xrange(0,3)] for i in xrange(1, self.nCancers+2) ]
		self.diagnosTime =[h.histo(self.expDur, -0.5, self.expDur - 0.5) for i in xrange(1, self.nCancers+1) ]
		self.nSick = [h.histo(self.expDur, -0.5, self.expDur-0.5) for j in xrange(0,self.nCancers+1)]
		self.nSurvival =[h.histo(self.expDur, -0.5, self.expDur - 0.5) for i in xrange(1, self.nCancers+1) ]


		self.nDie = h.histo(self.expDur, - 0.5, self.expDur - 0.5)
		self.nBirth = h.histo(self.expDur, - 0.5, self.expDur - 0.5)


		# self.canStage = [[h.histo(6, 0, 6) for i in xrange(0,self.nCancers+1)] for j in xrange(1, self.expDur+2)]

		self.readData()
		self.generateProbs()
		self.generateAgeDistrib()




	def initAgesAtPET(self):
		for age in xrange(1, len(self.agesUnderRad)+1):
			if age > self.minPetAge and age < self.maxPetAge:
				if age%self.period == 0:
					self.agesUnderRad[age-1] = 1


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
	
	def getProbSurvCancer(self, cancerIndex, stage):
		return self.probSurv[cancerIndex][stage-1]

	def generateAgeDistrib(self):
		numStat = int(self.nPeople)	
		self.ageDistrib = dict()
		for i in xrange(0,numStat):
			age = p.ageDistribution()
			# self.ageDistrib.update( { age : self.ageDistrib.get(age, 0) + 1 } )
			try:
				self.ageDistrib[age] += 1
			except KeyError:
				self.ageDistrib[age] = 1


		for key, value in self.ageDistrib.iteritems():
			self.ageDistrib[key] /= float(numStat)


	def updateAgeDistrib(self, num):
		for key, val in self.ageDistrib.iteritems():
			self.ageDistribFull[key] = int(val*num)
			# print key, self.ageDistribFull[key] 


	
		# print self.canProbs

	def genBirth(self, n):             # generate a number of kids to born
		nbirth = int(self.getNBirth())              # for example, if it's 3.4/1000 probability:
		dice = rnd.random()                         # it's 0.6 probability to born 3 and 0.4 - to born 4
		if dice < (self.getNBirth() - nbirth):      #
			return int((nbirth + 1.)/1000.*n)        #
		else:
			return int(nbirth/1000.*n)




	def ifDie(self, per):        # 0 for staying alive
		if per.age == 100:       # 1 for dying by age
			return 1			 # 2 for dying by cancer

		probDie = 0. 
		for i in per.cancers:     # check is it time to die 
			if i.stage == 4:
				return 2

		return 0 


		# dice = rnd.random()


		# if dice < (probDie):          # check probability 
		# 	return True
		# else:
		# 	return False 



##################################################################
	def generateEAR(self, doseVal, age, aae): # dose, attained age, age at exposure
		ear = []

		if aae < 30 + self.L:   
			eStar = 0
		else:
			eStar = (aae - self.L - 30)/10   

		for iCan in xrange(0, self.nCancers):
			if age < 20 + self.L:
				ear.append(0)
			else:	
				exponent = math.exp(self.getGamma(iCan) * eStar)
				attainedGuy = ( (age - self.L)/60. )**self.getEta(iCan)
				if self.ifBckg == 1:
					ear.append( self.getBetaS(0, iCan) * doseVal[iCan] * exponent * attainedGuy /10**7 )
				else:
					ear.append(0.)
		return ear


	def generateProbs(self):
		# file = open("ear.csv","w")
		for start in xrange(0,150):
			for age in xrange(1, 97):
				currentProb = [self.baselineRisk[i][age-1] for i in xrange(0, self.nCancers)]
				# currentProb = [0 for i in xrange(0, self.nCancers)]
				# if age < 25:
				# 	self.canProbs[start][age] = currentProb

				for ageAtExposure in xrange(start,age):
					if self.agesUnderRad[ageAtExposure-1] == 0:
						continue
					currEAR = self.generateEAR(self.petDose, age, ageAtExposure)
					for canType in xrange(0, self.nCancers):
						currentProb[canType] += currEAR[canType]
				# file.write(str(age)+','+str(currentProb)+'\n')
				self.canProbs[start][age] = currentProb
			# file.close()
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
				self.baselineRisk[canId][int(words[0]) - 1] = float(words[2]) / float(words[3])
				self.initialCan[int(words[0]) - 1][canId] = float(words[5])
				if canId == 0:
					self.probDeath[int(words[0]) -1] = float(words[1])*1000.
				words = []
		return

		

def regPopulation(info, people, lastDistr):
	peopleNew = []
	nFolk = len(people)
	# probRegulate = {1 : info.ageDistribFull[1] / float(nFolk)}
	probRegulate = dict()

	for i in xrange(1,101):
		# print i, lastDistr[i], info.ageDistribFull[i]
		probRegulate[i] = (lastDistr[i] - info.ageDistribFull[i]) 
		# print i, lastDistr[i], info.ageDistribFull[i], probRegulate[i]
		if probRegulate[i] < 0.: 
			for k in xrange(0, - probRegulate[i]):
				tempPer = p.person()           #  create new temporary person
				tempPer.age = i                     # set his age to 0 
				tempPer.startAge = i                
				tempPer.probDeath = info.getProbDeath(tempPer.age)

				tempPer.info = info ################## temp

				tempPer.initCancer()
				
				# info.nBirth.fill(j)
				peopleNew.append(cp.copy(tempPer)) 

	for j in people:
		if probRegulate[j.age] > 0.:
			dice = rnd.random()
			# print dice, probRegulate[j.age]
			if dice < probRegulate[j.age] / float(lastDistr[j.age]):
				continue

		peopleNew.append(j)

	return peopleNew

