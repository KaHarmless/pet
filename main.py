import person
import data
import matplotlib.pyplot as mpl
import random as rnd
import copy as cp


# histogramming

# for i in age:
# 	nSick.append(0)

# people

nPeople = 10**5
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



x = xrange(0,200)
y = []
# for i in x:
	# y.append(0)

# main loop

# while len(people) != 0:
for j in xrange(0,200):
	time.append(j)
	# nSickArr.append(0)
	nSick = 0
	nFolk = len(people)

	avAge = 0
	# print j

	# x.append(j)
	# y.append(len(people))

	if j%10 == 0:
		print ">>>",j

	temp = 0.



	peopleNew = []
	###############################################################################
	for i in people:             # loop for each person every year
		if i.age >= 100:
			# print "YOU DIED"
			nHealthy += 1
			# i.info.probDeath = 30.
			continue

		# print people.index(i),i.age

		for j in xrange(0,len(i.cancers)):
			# print i.ageGetCancer[j]
			if (i.age - i.ageGetCancer[j]) == 1:
				temp += 1.



		avAge += i.age

		# if len(i.cancers) != 0 and j > 100:
		# 	nSick += 1
		# 	nSickAge[i.age]+=1
		# 	continue

		# if j == 400:
			# print  people.index(i),i.age


		# if i.toDie:
		# 	people.pop(people.index(i))
		# 	continue
		
		if i.info.ifDie(i):      # getting probabiluty to die and check
			# print i.age
			# NN[i.age] += 1
			continue                    # go to the next person

		peopleNew.append(i)
		i.increaseAge()          # increase age of person
	##########################################################################################
	# print temp
	
	# y[j] = temp

	y.append(temp/len(people))

	people = peopleNew

	nSickArr.append(100.*nSick/nFolk)
	avAge /= nFolk
	NN[int(avAge)] += 1

	sick = 0.
	if j == 102:
		for i in people:
			# y[i.age]+=1
			# for j in xrange(0,len(i.cancers)):
				# y[i.ageGetCancer[j]] += 1
			if len(i.cancers) != 0:
				sick += 1.
		print "number of people:", len(people)
		print "number of sick:", sick / len(people)




	if len(people) < 1 :
		nFolk = 0
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
# x = ageSick
# y = NN
# y = nSickAge


plotOutput = open("data.csv","w")
for i in xrange(0,len(x)):
	plotOutput.write(str(x[i])+","+str(y[i])+"\n")
plotOutput.close()


mpl.plot(x,y)
mpl.show()


