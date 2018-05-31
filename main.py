import person
import data
import matplotlib.pyplot as pl
import random as rnd
import copy as cp


# people

info = data.data(0) # baseline flag: 0 - only background, 1 - only PET, 2 - sum
############################## temp



nPeople = 10**4        ####################
expDur = 300           ####################




############################ initial cohort ##############
people = []
for i in range(0,nPeople):
	newPerson = person.person()
	newPerson.info = info
	newPerson.probDeath = info.getProbDeath(newPerson.age)
	# newPerson.age = person.ageDistribution()
	newPerson.index = 1
	# newPerson.startAge = person.ageDistribution()
	people.append(cp.copy(newPerson))  #initial group of people

print ">>> Initial cohort is ready"

##########################################################




x = xrange(0,expDur+1)

# x = xrange(1, 120)


y = [[0 for i in x] for j in xrange(0,info.nCancers+1)]
N = [0 for i in x]

# z = [[0 for i in x] for j in xrange(0,6)]
# nz = [0 for j in xrange(0,6)]


################ main loop by years of experiment ###############

for j in xrange(1,expDur + 1):

	nFolk = len(people)

	N[j-1] = nFolk

	if j%20 == 0 and j != 0:
		print ">>>", j


	
	###############################################################################
	peopleNew = []

	for i in people:             # loop for each person every year
		if i.age > 140:
			print "I'm lucky man! My age is", i.age, "years!\n I was born in", i.startAge, "!"
		# if i.age >= 96:
			# probDeath
			
		for k in xrange(0,len(i.cancers)):
			if (i.age - i.cancers[k].startAge) == 1:
				y[i.cancers[k].cancerType][j] += 1.
				# pass


		if info.ifDie(i):      # getting probabiluty to die and check
			continue                    # go to the next person

		
		i.increaseAge()          # increase age of person
		peopleNew.append(i)
		
	people = peopleNew
	##########################################################################################
	

	for k in xrange(1, 6):
		y[6][j] += y[k][j]

	for i in y:
			i[j] /= nFolk 
			i[j] *= 10000.


	# for k in y:
	# 	k[j] /= nFolk

	if len(people) < 1 :
		nFolk = 0
		break
	

	# for j in xrange(0, people[0].info.genBirth(len(people))):  # do the loop as much times as a number of people to born
	for k in xrange(0, info.genBirth(nFolk)):
		tempPer = person.person()           # create new temporary person
		tempPer.age = 1                     # set his age to 0 
		tempPer.startAge = j                 # and starting age too
		tempPer.probDeath = info.getProbDeath(tempPer.age)

		tempPer.info = info ################## temp

		people.append(cp.copy(tempPer))              # add out temporary man to the list

#####################################################################

# for j in x: #xrange(0,len(x)):
# 	# for k in xrange(0, len(norm)):
# 	norm[0] += y[0][j]
# 	norm[6] += y[6][j]

# for j in x:#xrange(0,len(x)):
# 	y[0][j] /= norm[0]
# 	y[6][j] /= norm[6]

# for i in xrange(0,3):
# 	for j in z[i]:
# 		j /= nz[i]




# plotOutput = open("data.csv","w")
# plotOutput.write("age,all(danger),lungs,colon,stomach,liver,bladder\n")
# for i in xrange(0,len(x)):
# 	# msg = str(x[i])+','
# 	# for j in xrange(1, len(y)-1):
# 		# msg += str(y[j][i]) + ','
# 	# msg += '\n'
# 	plotOutput.write(str(x[i])+','+str(y[0][i])+','+str(y[1][i])+','+str(y[2][i])+','+str(y[3][i])+','+str(y[4][i])+','+str(y[5][i])+'\n')
# plotOutput.close()

# # pl0 = pl.plot(x,y[0], color = "red", label = "All cancers")
# pl1 = pl.plot(x,y[1], color = "green", label = "Lungs cancer")
# pl2 = pl.plot(x,y[2], color = "blue", label = "Colon cancer")
# pl3 = pl.plot(x,y[3], color = "cyan", label = "Stomach cancer")
# pl4 = pl.plot(x,y[4], color = "magenta", label = "Liver cancer")
# pl5 = pl.plot(x,y[5], color = "brown", label = "Bladder cancer")
# pl6 = pl.plot(x,y[6], color = "black", label = "Summ of solid cancers")

# pl0 = pl.plot(x,z[0], color = "red", label = "110th year")
# pl1 = pl.plot(x,z[1], color = "green", label = "200th year")
# pl2 = pl.plot(x,z[2], color = "blue", label = "300th year")


pl.plot(x,N)

# allSolid = pl.plot(x,y[0], color = "red", label = "All solid cancers")
# sumSolid = pl.plot(x,y[6], color = "blue", label = "Summ of 5 cancers")

# allSolid = pl.plot(x,y[0], color = "red", label = "All solid cancers")
# sumSolid = pl.plot(x,y[6], color = "blue",label = "Summ of 5 cancers")



pl.legend()
pl.show()