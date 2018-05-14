import random as rnd

class data(object):
	# lungs, colon, prostate, liver, bladder
	betam = [2.3, 3.2, 0.11, 2.2, 1.2]
	# betam = [2.3, 0, 0, 0, 0]
	# betam = [2.3, 1., 0.11, 2.2, 1.2]       # beta for males
	betaf = [0,0,0,0,0]                     # beta for females
	eta = [5.2, 2.8, 2.8, 4.1, 6.]          # eta
	gamma = [-0.41, -0.41, -0.41, -0.41, -0.41,] # gamma 

	probDeathCancer = [7, 7, 7, 7, 7]        # number of people to die from cancer for every type of cancer (per 1000)

	probDeath =  8.44                          # probability to die just because (n per 1000) 

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

	def getProbDeath(self):
		return self.probDeath
	
	def getProbDeathCancer(self,i):
		return self.probDeathCancer[i]

	def __init__(self):
		pass

	def genBirth(self, n):             # generate a number of kids to born
		nbirth = int(self.getNBirth())              # for example, if it's 3.4/1000 probability:
		dice = rnd.random()                         # it's 0.6 probability to born 3 and 0.4 - to born 4
		if dice < (self.getNBirth() - nbirth):      #
			return int((nbirth + 1)/1000.*n)             #
		else:
			return int(nbirth/1000.*n)




	def ifDie(self, per):             # check is it time to die     
		dice = rnd.random()
		prob = self.getProbDeath()     # getting probability
		# for i in per.cancers:          # loop for all of his cancers
		# 	prob += self.getProbDeathCancer(i.cancerType)   # add corresponding risk of death for his cancers
		# print str(dice) + ' ' + str(prob/1000.)
		if dice < prob/1000.:          # check probability 
			return True
		else:
			return False 


