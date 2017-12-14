import copy

txt_file = open('chat.txt', 'r')
lines = txt_file.readlines()

def getContent(line):
	return line[20:][ len(line[20:].split(':')[0])+ 2 : ]

def getDate(line):
	return line[:20].split(',')[0]

def getUser(line):
	return line[20:].split(':')[0].strip()

def checkIsNewMsg(line_p):
	line = copy.copy(line_p)
	return len( line[20:].split(':') ) != 1

def processLine(txt):
	txt = txt.lower()
	return txt.replace('\n', ' ')

def getQA(lines):
	Q = []
	A = []
	lastDate = ''
	tempQ = ''
	tempA = ''
	lastUpdated = 'A'
	lastUser = ''
	for line in lines:
		if checkIsNewMsg(line):
			# print line
			currUser = getUser(line)
			if lastUser != currUser:
				lastUser = currUser
				if lastUpdated == 'Q':
					lastUpdated = 'A'
				else:
					lastUpdated = 'Q'
					if tempQ != '' and tempA != '':
						Q.append(processLine(tempA))
						A.append(processLine(tempQ))

					tempQ, tempA = '', ''

			currDate = getDate(line)
			if currDate != lastDate :
				# print (tempA, tempQ)
				# print "#"
				if tempQ != '' and tempA != '':
					Q.append(processLine(tempA))
					A.append(processLine(tempQ))

				lastDate = currDate
				tempQ, tempA = '', ''

			else:
				if lastUpdated == 'A':
					tempQ = tempQ + getContent(line)
				else:
					tempA = tempA + getContent(line)

				lastUpdated = 'A' if lastUpdated == 'Q' else 'Q'
		else:
			if lastUpdated == 'A':
				tempA = tempA + getContent(line)
			else:
				tempQ = tempQ + getContent(line)
	return (Q, A)

def saveToFile(QA):
	q_file = open('i_ques.txt', 'w')
	a_file = open('i_ans.txt', 'w')
	vocab_file = open('i_vocab.txt', 'w')
	vocab = []
	print "Writing to i_ques.txt"
	for i in QA[0]:
		for word in i.split(' '):
			if word not in vocab:
				vocab.append(word)
		q_file.write(i+'\n')
	print "writing to ans.txt"
	for i in QA[1]:
		for word in i.split(' '):
			if word not in vocab:
				vocab.append(word)
		a_file.write(i+'\n')

	print "writing to vocab.txt"
	for i in vocab:
		vocab_file.write(i+'\n')

qa = getQA(lines)
print len(qa[1])
saveToFile(qa)
