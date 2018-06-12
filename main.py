#!/usr/bin/python

import matplotlib.pyplot as plt
import person
import data
import histo as h
import random as rnd
import copy as cp

# people


############################## temp

                       ##########################################
T = 1                  # T means period of PET (once a T years) #        
MODE = 1               # PET impact:    0 - only background    ,#
                       # (MODE)         1 - background + pet    #
nPeople = 10**5        ##########################################


print "Experiment for:\t", nPeople, " people"
print "With period:\t", T, "years"
print "Mode: \t\t",MODE  

############################ initial cohort ##############
info = data.data(MODE, T) # 
people = []
for i in range(0,nPeople):
	newPerson = person.person()
	newPerson.info = info
	newPerson.probDeath = info.getProbDeath(newPerson.age)
	# newPerson.age = person.ageDistribution()
	if newPerson.age > 20:
		newPerson.index = 1
	# newPerson.startAge = person.ageDistribution()
	people.append(cp.copy(newPerson))  #initial group of people

print ">>> Initial cohort is ready"

##########################################################



expDur = info.expDur   ####################






x = xrange(0, expDur)

# x = xrange(1, 120)


y = [h.histo(expDur, -0.5, expDur-0.5) for j in xrange(0,info.nCancers+1)]

N = h.histo(200, 0, expDur+2)   # initialization h.histo(nBins, xMin , xMax)

Population = []
# canAges = [0 for i in xrange(0,100)]



# z = [[0 for i in x] for j in xrange(0,6)]
# nz = [0 for j in xrange(0,6)]


################ main loop by years of experiment ###############

firstSick = False
firstSickYear = 0

for j in xrange(1,expDur + 1):

	nFolk = len(people)
	Population.append(nFolk)

	 # filling hist with numbers of people
	# N.fill(nFolk)

	if j%20 == 0 and j != 0:
		print ">>>", j


	
	###############################################################################
	peopleNew = []

	for i in people:             # loop for each person every year
		i.date = j

		N.fill(j)   # age distribution

		if info.ifDie(i):      # getting probability to die and check
			info.nDie.fill(j)
			continue                    # go to the next person


		i.increaseAge()          # increase age of person

		peopleNew.append(i)
		
	people = peopleNew
	##########################################################################################
	





	if len(people) < 1 :
		nFolk = 0
		break
	

	# for j in xrange(0, people[0].info.genBirth(len(people))):  # do the loop as much times as a number of people to born
	for k in xrange(0, info.genBirth(nFolk)):
		tempPer = person.person()           #  create new temporary person
		tempPer.age = 1                     # set his age to 0 
		tempPer.startAge = j                 # and starting age too
		tempPer.probDeath = info.getProbDeath(tempPer.age)

		tempPer.info = info ################## temp
		info.nBirth.fill(j)
		people.append(cp.copy(tempPer))              # add out temporary man to the list

#####################################################################

# N.makeRegHist()
# info.nDie.makeRegHist()
# info.nBirth.makeRegHist()

# N.draw(color = 'red', label = "Population over time")
# nDie.draw(rootLike = True, color = 'blue', label = "Dying per year")
# N.draw(normalized = True)

info.diagnosTime[5].makeZero()
info.nSick[6].makeZero()

for k in xrange(1, 6):
	y[6].histAdd(y[k])
	info.nSick[6].histAdd(info.nSick[k])

for k in xrange(0, 5):
	info.diagnosTime[5].histAdd(info.diagnosTime[k])





for i in xrange(1, info.nCancers+1):
	y[i].makeRegHist()
	info.nSick[i].makeRegHist()


for i in xrange(0, info.nCancers):
	info.diagnosTime[i].makeRegHist()
	info.nSurvival[i].makeRegHist()

for j in info.canStage:
	for k in j:
		k.makeRegHist()


# print len(y[6].x), len(y[6].y)
for j in xrange(1, info.nCancers+1):
	for i in xrange(firstSickYear, y[1].nBins):
		try:
			d = y[j].getBinContent(i) / Population[i-firstSickYear] * 10000.
			y[j].setBinContent(i, d)
			
			c = info.diagnosTime[j-1].getBinContent(i) / Population[i-firstSickYear] * 10000.
			info.diagnosTime[j-1].setBinContent(i, c)

			a = info.nSurvival[j-1].getBinContent(i) / Population[i-firstSickYear] * 10000.
			info.nSurvival[j-1].setBinContent(i, a)
			
			e = info.nSick[j].getBinContent(i) / Population[i-firstSickYear] * 10000.
			info.nSick[j].setBinContent(i, e)

			for k in info.canStage[j]:
				f = k.getBinContent(i) / Population[i] * 10000.
				k.setBinContent(i, f)

		except IndexError:
			print "whoops..."
			continue

		# info.nSick[6].x = cp.copy(x)
		# info.nSick[6].generateData()
		# info.nSick[6].makeZero()
		# info.nSick[6].makeRootHist()
		# info.diagnosTime[5].x = cp.copy(x)
		# info.diagnosTime[5].generateData()
		# info.diagnosTime[5].makeZero()
		# info.diagnosTime[5].makeRootHist()





		




info.nSick[1].draw(color = "red", label = "Lung cancer")
# info.nSick[2].draw(color = "green", label = "Colon cancer")
# info.nSick[3].draw(color = "blue", label = "Stomach cancer")
# info.nSick[4].draw(color = "cyan", label = "Liver cancer")
# info.nSick[5].draw(color = "magenta", label = "Bladder cancer")

# info.nSick[6].draw(color = "black", label = "Have got cancer last year (per 10k)")

# info.nSick[6].draw(color = "red", label = "Have got cancer last year (per 10k)")




# info.canStage[6][0].draw(color = "red", label = "First stage")
# info.canStage[6][1].draw(color = "green", label = "Second stage")
# info.canStage[6][2].draw(color = "blue", label = "Third stage")
# info.canStage[3].draw(color = "cyan", label = "Liver cancer")
# info.canStage[4].draw(color = "magenta", label = "Bladder cancer")
# info.canStage[5].draw(color = "black", label = "Sum")




# for i in xrange(0, info.nCancers-1):
# 	info.diagnosTime[i].makeRootHist()

# info.diagnosTime[6].makeRootHist()

info.diagnosTime[0].draw(color = "blue", label = "Lung cancer")
# info.diagnosTime[1].draw(color = "green", label = "Colon cancer")
# info.diagnosTime[2].draw(color = "blue", label = "Stomach cancer")
# info.diagnosTime[3].draw(color = "cyan", label = "Liver cancer")
# info.diagnosTime[4].draw(color = "magenta", label = "Bladder cancer")
# info.diagnosTime[5].draw(color = "red", label = "Have detected cancer last year (per 10k)")

# info.diagnosTime[5].draw(color = "blue", label = "Have detected cancer last year (per 10k)")




info.nSurvival[0].draw(color = "green", label = "Lung cancer")
# info.nSurvival[1].draw(color = "green", label = "Colon cancer")
# info.nSurvival[2].draw(color = "blue", label = "Stomach cancer")
# info.nSurvival[3].draw(color = "cyan", label = "Liver cancer")
# info.nSurvival[4].draw(color = "magenta", label = "Bladder cancer")
# info.nSurvival[5].draw(color = "black", label = "Total (per 10k)")

# info.nSurvival[5].draw(color = "green", label = "Healed last year (per 10k)")


# z = [[info.diagnosTime[i][j]/y[i][j] for i in xrange(1,6)] for j in xrange(0,y.nBins)]:


# zh = [h.histo(210, -0.5, 210 - 0.5) for i in xrange(1, info.nCancers+1)]

# for i in xrange(1,5):
# 	for j in xrange(0,y[1].nBins):
# 		if (y[i].y[j] == 0):
# 			continue
# 		zh[i].y.append(info.diagnosTime[i].y[j]/y[i].y[j])
# 		zh[i].x.append(y[i].x[j])



 


# zh[1].draw(color = "red", label = "Lung cancer (N diased / N sick)")
# zh[2].draw(color = "green", label = "Colon cancer (N diased / N sick)")
# zh[3].draw(color = "blue", label = "Stomach cancer (N diased / N sick)")
# zh[4].draw(color = "cyan", label = "Liver cancer (N diased / N sick)")
# zh[5].draw(color = "magenta", label = "Bladder cancer (N diased / N sick)")



sickOutput = open("gotSickPY.csv","w")
sickOutput.write("age,lungs,colon,stomach,liver,bladder,sum\n")
for i in xrange(0,len(x)):
	msg = str(x[i])+','
	for j in xrange(1, len(info.nSick)):
		msg += str(info.nSick[j].y[i]) + ','
	msg += '\n'
	# msg += ',,' + str(N.y[i]) + ','+ str(info.nBirth.y[i])+ ','+ str(info.nDie.y[i])+ '\n'
	sickOutput.write(msg)
sickOutput.close()

detectedOutput = open("gotDetectedPY.csv","w")
detectedOutput.write("age,lungs,colon,stomach,liver,bladder,sum\n")
for i in xrange(0,len(x)):
	msg = str(x[i])+','
	for j in xrange(0, 6):
		msg += str(info.diagnosTime[j].y[i]) + ','
	msg += '\n'
	detectedOutput.write(msg)
detectedOutput.close()

survivalOutput = open("survivalPY.csv","w")
survivalOutput.write("age,lungs,colon,stomach,liver,bladder,sum\n")
for i in xrange(0,len(x)):
	msg = str(x[i])+','
	for j in xrange(0, 6):
		msg += str(info.nSurvival[j].y[i]) + ','
	msg += '\n'
	survivalOutput.write(msg)
survivalOutput.close()

stageOutput = open("gotStagesPY.csv","w")
stageOutput.write('age,lungs,colon,stomach,liver,bladder,sum,'+
				  'second,lungs,colon,stomach,liver,bladder,sum,'+
				  'third,lungs,colon,stomach,liver,bladder,sum,\n')
for i in xrange(0,len(x)):
	msg = str(x[i])+','
	for j in xrange(0, 3):
		for k in xrange(1,7):
			msg += str(info.canStage[k][j].y[i]) + ','
		msg += ','
	msg += '\n'
	stageOutput.write(msg)
stageOutput.close()



# self.info.canStage[i.cancerType-1].fill(i.stage)


h.finish()


