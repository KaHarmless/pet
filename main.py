#!/usr/bin/python

import matplotlib.pyplot as plt
import person
import data
import histo as h
import random as rnd
import copy as cp





                       ##########################################
T = 1                  # T means period of PET (once a T years) #        
MODE = 0               # PET impact:    0 - only background    ,#
                       # (MODE)         1 - background + pet    #
				       ##########################################

info = data.data(MODE, T) # 

					   ################################
nPeople = info.nPeople # NUMBER OF PEOPLE SET IN DATA #
					   ################################

print "Experiment for:\t", nPeople, " people"
print "With period:\t", T, "years"
print "Mode: \t\t",MODE  


################### Initial cohort creation ######################

people = []
for i in range(0,nPeople):
	newPerson = person.person()
	newPerson.info = info
	newPerson.probDeath = info.getProbDeath(newPerson.age)
	# newPerson.age = person.ageDistribution()
	if newPerson.age > 20:
		newPerson.index = 1
	newPerson.initCancer()
	# newPerson.startAge = person.ageDistribution()
	people.append(cp.copy(newPerson))  #initial group of people

print ">>> Initial cohort is ready"
############# End of initial cohort creation #####################

expDur = info.expDur   ####################




x = xrange(0, expDur)

# x = xrange(1, 120)


y = [h.histo(expDur, -0.5, expDur-0.5) for j in xrange(0,info.nCancers+1)]

N = h.histo(200, 0, expDur+2)   # initialization h.histo(nBins, xMin , xMax)

Population = []
# canAges = [0 for i in xrange(0,100)]



# z = [[0 for i in x] for j in xrange(0,6)]
# nz = [0 for j in xrange(0,6)]


firstSick = False
firstSickYear = 0

info.updateAgeDistrib(nPeople)
lastDistr = info.ageDistribFull

nFolk = nPeople


################ Main loop by years of experiment ###############
for j in xrange(1,expDur + 1):
	# print len(people)
	info.updateAgeDistrib(nPeople)
	# if j != 1:
	newPeople = data.regPopulation(info, people, lastDistr)
	people = newPeople

	lastDistr = {i : 0 for i in xrange(1,101)}

	nFolk = len(people)
	Population.append(nFolk)


	# info.updateAgeDistrib(nFolk)

	 # filling hist with numbers of people
	# N.fill(nFolk)

	if j%20 == 0 and j != 0:
		print ">>>", j


	
	################################# Loop by people #################################
	peopleNew = []

	for i in people:             # loop for each person every year
		i.date = j

		N.fill(j)   # age distribution

		dyingCond = info.ifDie(i)  # getting probability to die
		if dyingCond == 2:         # dying by cancer
			if i.age >= info.minPetAge and i.age <= info.maxPetAge:
				info.nDie.fill(j)
			continue                    # go to the next person
		elif dyingCond == 1:       # dying by age
			continue

		lastDistr[i.age + 1] += 1 
		# print lastDistr[i.age + 1] 

		i.increaseAge()          # increase age of person

		peopleNew.append(i)

	lastDistr[1] = 0
	people = peopleNew
	################################ End of loop by people ###############################
	

	if len(people) < 1 :
		nFolk = 0
		break
	# print nFolk, info.genBirth(nFolk)

	# for j in xrange(0, people[0].info.genBirth(len(people))):  # do the loop as much times as a number of people to born
	for k in xrange(0, info.genBirth(nFolk)):
		tempPer = person.person()           #  create new temporary person
		tempPer.age = 1                     # set his age to 0 
		tempPer.startAge = 1                
		tempPer.probDeath = info.getProbDeath(tempPer.age)

		tempPer.info = info ################## temp
		info.nBirth.fill(j)
		people.append(cp.copy(tempPer))              # add out temporary man to the list
############################ End of loop by years #################################



########### Adding histos for total full-body data ####
info.diagnosTime[5].makeZero()
info.nSick[6].makeZero()

for k in xrange(1, 6):
	y[6].histAdd(y[k])
	info.nSick[6].histAdd(info.nSick[k])

for k in xrange(0, 5):
	info.diagnosTime[5].histAdd(info.diagnosTime[k])
################## End of histo adding ################ 

##################### Histogram processing ##############
info.nDie.makeRegHist()

for i in xrange(1, info.nCancers+1):
	y[i].makeRegHist()
	info.nSick[i].makeRegHist()


for i in xrange(0, info.nCancers):
	info.diagnosTime[i].makeRegHist()
	info.nSurvival[i].makeRegHist()

for j in info.canStage:
	for k in j:
		k.makeRegHist()
############ End of histogram processing ##################


############### Normalization per 10k of population ######
# for i in xrange(firstSickYear, y[1].nBins):

for i in xrange(firstSickYear, info.nDie.nBins):
	g = info.nDie.getBinContent(i) / Population[i-firstSickYear] * 10000.
	info.nDie.setBinContent(i, g)

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
########## End of histogram normalization ###################


# info.nSick[1].draw(color = "red", label = "Lung cancer")

############################# Exporting to files #################################
print "Exporting results to files...\n"

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


deathRateFile = open("deathRatePY.csv","w")
deathRateFile.write('year, rate\n')
for i in xrange(0,len(x)):
	msg = str(x[i]) + ',' + str(info.nDie.y[i]) + ',\n'
	deathRateFile.write(msg)
deathRateFile.close()
########################## End of file export ################################


# self.info.canStage[i.cancerType-1].fill(i.stage)


# h.finish()


