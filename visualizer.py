def displayShortestAnswer(data):
	print ("A:%s"%(data['body']))

	print ("Q:%s"%(data['question']))

	print ("length:%s characters"%(data['length']))


def displayMostActiveUsers(data):
	index = 1
	for u in data:
		print ("%s - %s (%s)"%(index,u[0],u[1]))
		index +=1


def displayMostActiveTopics(data):
	index = 1
	for u in data:
		print ("%s - %s (%s)"%(index,u[0],u[1]))
		index +=1


def displayMostHelpfulUsers(data):
	index = 1
	for u in data:
		print ("%s - %s (%s)"%(index,u[0],u[1]))
		index +=1



def displayMostAnsweredQuestions(data):
	index = 1
	for u in data:
		print ("%s - %s (%s)"%(index,u[0],u[1]))
		index +=1




def displayMostCommonPhrases(data):
	index = 1
	for u in data:
		print ("%s - %s (%s)"%(index,u[0],u[1]))
		index +=1




