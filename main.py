import person
import data
import matplotlib.pyplot as mpl
import random as rnd
import copy as cp


# histogramming

# for i in age:
# 	nSick.append(0)

# people

nPeople = 10**6
people = [ person.person() for i in range(0,nPeople)]  #initial group of people

ageSick = range(0,101)

time = []
nSickArr = []

nSickAge = []

NN = []

for i in ageSick:
	nSickAge.append(0.)
	NN.append(0.)

nHealthy = 0



# main loop

# while len(people) != 0:
for j in xrange(0,500):
	time.append(j)
	# nSickArr.append(0)
	nSick = 0
	nFolk = len(people)

	avAge = 0
	# print j
	
	

	###############################################################################
	for i in people:             # loop for each person every year
		# NN[i.age] += 1

		if len(i.cancers) != 0 :
			nSick += 1
			# nSickArr[-1] += 1.
			nSickAge[i.age]+=1
			people.pop(people.index(i))
			continue

		if i.age == 100:
			# print "YOU DIED"
			nHealthy += 1
			people.pop(people.index(i))
			continue

		# if i.toDie:
		# 	people.pop(people.index(i))
		# 	continue
		
		if i.info.ifDie(i):      # getting probabiluty to die and check
			# print i.age
			# NN[i.age] += 1
			people.pop(people.index(i)) # deleting the person from the list if he dies
			continue                    # go to the next person

		avAge += i.age

		i.increaseAge()          # increase age of person
	##########################################################################################
	
	nSickArr.append(100.*nSick/nFolk)
	avAge /= nFolk
	NN[int(avAge)] += 1
	
	if len(people) == 0 :
		break
	for j in xrange(0, people[0].info.genBirth(len(people))):  # do the loop as much times as a number of people to born
		tempPer = person.person()           # create new temporary person
		tempPer.age = 1                     # set his age to 0 
		tempPer.startAge = 1                # and starting age too
		people.append(cp.copy(tempPer))              # add out temporary man to the list
		nPeople +=1
	




	###################################



# print 100. - nHealthy*100./len(people)


# mpl.plot(time,nSickArr)
# mpl.plot(ageSick,nSickAge)
mpl.plot(ageSick,NN)
mpl.show()


