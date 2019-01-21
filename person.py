import cancer
import random
import data
import math
import histo as h
import copy as cp

class person(object):


	def __init__(self): 
		self.info = 0          # data object, our data container
		# initial parameters of person
		self.sex = 0

		self.date = 1

		self.index = 0

		self.cancers = []

		self.age = self.generateAge()    # generate age
		self.startAge = self.age         # save initial age

		self.ageGetCancer = []

		self.badMarker = False
		# for i in xrange(0,self.startAge):
		# 	self.dose.append(0)



	def generateAge(self):
		return ageDistribution()



	def increaseAge(self):         #################################

		if self.info.agesUnderRad[self.age-1] == 1:
			self.diagnostics()						# try to detect 
		self.canTreat()

		for i in self.cancers:                  # update tumors                
			if i.isFound:
				if self.age >= self.info.minPetAge and self.age <= self.info.maxPetAge:
					self.info.canStage[i.cancerType][i.stage-1].fill(self.date)
					self.info.canStage[6][i.stage-1].fill(self.date)
			i.ownerAge = self.age
			i.grow()


		self.isGettingCancer()                  # check for new cancer
		self.age += 1                           # increment age



	def diagnostics(self):
		for i in self.cancers:
			if i.stage == 0 or i.isFound:
				continue
			dice = random.random()
			if dice < (self.info.probDetect[i.cancerType][i.stage - 1]/100.):
				i.isFound = True
				i.ageFound = self.age
				# self.info.canStage[self.date][i.cancerType-1].fill(i.stage-1)
				if self.age >= self.info.minPetAge and self.age <= self.info.maxPetAge:
					self.info.diagnosTime[i.cancerType].fill(self.date)
				# self.info.canStage[i.cancerType-1].fill(i.stage-1)



	def isGettingCancer(self):
		# if self.age < 20:            # no cancer under 20 
			# return
			
		# self.generateProb()  ################# temp
		if self.age < 96:
			self.cancerProb = self.info.canProbs[self.startAge-1][self.age]
		else:
			self.cancerProb = self.info.canProbs[self.startAge-1][95]
		# print self.cancerProb

		for iCan in xrange(1, self.info.nCancers):
			dice = random.random()   # get random value
			if dice < self.cancerProb[iCan]:
				self.makeCancer(iCan)
				# if self.age >= 70:                        # 70+ CUTOFF
					# continue
				# if self.age >= self.info.minPetAge and self.age <= self.info.maxPetAge:
				self.info.nSick[iCan].fill(self.date)


	def canTreat(self):
		newCancerList = []
		for i in self.cancers:
			if i.isFound:
				prob = i.info.getProbSurvCancer(i.cancerType, i.stage)/100.
				dice = random.random()   # get random value
				if dice > prob:
					newCancerList.append(i)
				else:
					if self.age >= self.info.minPetAge and self.age <= self.info.maxPetAge:
						self.info.nSurvival[i.cancerType].fill(self.date)
						self.info.nSurvival[6].fill(self.date)
			else:
				newCancerList.append(i)
		self.cancers = None
		self.cancers = cp.copy(newCancerList)




################### Generating probabilities of getting cancer #################

	# def generateEAR(self, doseVal, age, aae): # dose, attained age, age at exposure
	# 	ear = []
	# 	if aae < 30:   
	# 		eStar = 0
	# 	else:
	# 		eStar = (aae - self.info.L - 30)/10    
	# 	for iCan in xrange(0,self.info.nCancers):
	# 		if age < 20:
	# 			ear.append(0)
	# 		else:	
	# 			exponent = math.exp(self.info.getGamma(iCan) * eStar)
	# 			attainedGuy = ( (age - self.info.L)/60. )**self.info.getEta(iCan)
	# 			ear.append( self.info.getBetaS(self.sex, iCan) * doseVal[iCan] * exponent * attainedGuy /10**7 )
	# 	return ear
			
	# def generateProb(self):
	# 	tempProb = [0 for i in xrange(0, self.info.nCancers)]
	# 	for ageAtExposure in xrange(0, self.age):
	# 		currEAR = self.generateEAR(self.info.petDose, self.age, ageAtExposure)
	# 		for canType in xrange(0, self.info.nCancers):
	# 			tempProb[canType] += currEAR[canType]
	# 	self.cancerProb = tempProb
	# 	for i in xrange(0, self.info.nCancers):
	# 		if tempProb[0] > 1:
	# 			print "---> Danger! Probability of getting cancer is more then 1!"
	# 	return

################################################################################


	def makeCancer(self, i):      # make a cancer
		newCancer = cancer.cancer(i,self.age)
		newCancer.cancerName = self.info.cancerName[i]
		newCancer.info = cp.copy(self.info)
		self.cancers.append(cp.copy(newCancer))
		newCancer = None
		self.ageGetCancer.append(self.age)

		


	def initCancer(self):
		if self.age < 96:
			self.cancerProb = self.info.initialCan[self.age]
		else:
			self.cancerProb = self.info.initialCan[95]


		for iCan in xrange(1, self.info.nCancers):
			dice = random.random()   # get random value
			if dice < self.cancerProb[iCan]:
				self.makeCancer(iCan)




# def ageDistribution():  # generating age of person due to distribution
# 	dice = random.random();
# 	return 20
# 	if dice < 0.1873 :
# 		return int(0 + random.random()*14)
# 	if dice < 0.32 :
# 		return int(15 + random.random()*9)
# 	if dice < 0.7145 :
# 		return int(25 + random.random()*29)
# 	if dice < 0.8436 :
# 		return int(55 + random.random()*9)
# 	else:
# 		return int(65 + random.random()*15)

def ageDistribution():  # generating age of person due to distribution
	dice = random.random();
	# return 20
	if dice < 0.055307:
		return random.randint(1,4)
	if dice < 0.141667 :
		return random.randint(5,9)
	if dice < 0.214697 :
		return random.randint(10,14)
	if dice < 0.286865 :
		return random.randint(15,19)
	if dice < 0.353343 :
		return random.randint(20,24)
	if dice < 0.417873 :
		return random.randint(25,29)
	if dice < 0.488917 :
		return random.randint(30,34)
	if dice < 0.56968 :
		return random.randint(35,39)
	if dice < 0.651532 :
		return random.randint(40,44)
	if dice < 0.723649 :
		return random.randint(45,49)
	if dice < 0.786366 :
		return random.randint(50,54)
	if dice < 0.834821 :
		return random.randint(55,59)
	if dice < 0.873615 :
		return random.randint(60,64)
	if dice < 0.907879 :
		return random.randint(65,69)
	if dice < 0.939651 :
		return random.randint(70,74)
	if dice < 0.966649 :
		return random.randint(75,79)
	if dice < 0.984491 :
		return random.randint(80,84)
	else:
		return random.randint(85,100)