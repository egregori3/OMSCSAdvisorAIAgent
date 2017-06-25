import requests

#Example usage
#import QnAMaker
#
#TestQnAMaker = QnAMaker.QnAMaker( KBid='insert Knowledge Base ID', \
#				   SubKey='insert Subscription Key')
#
#	ReturnCode = TestQnAMaker.Request('insert question here')
#	print " - ReturnCode: ", ReturnCode
#	if( ReturnCode == 200 ):
#		answer = TestQnAMaker.GetNextAnswer()
#		print "Score: ", answer['score']
#		print "Answer:"
#		print answer['answer']
class QnAMaker(object):
	host = "https://westus.api.cognitive.microsoft.com/qnamaker/v2.0"
	answers = None
	answerIndex = 0
	

	def __init__(self, KBid, SubKey):
		self.KnowledgeBaseID = KBid
		self.SubscriptionKey = SubKey

	def Request(self,Question):
		self.answers = None
		url = "/knowledgebases/"
		url += self.KnowledgeBaseID
		url += "/generateAnswer" 
		header = {'Ocp-Apim-Subscription-Key':self.SubscriptionKey}
		header.update( {'Content-Type':'application/json'} )
		data = {'question':Question}

		r = requests.post(self.host+url,headers=header,json=data)

		# r.text = {"answers":[{"answer":"Hello","questions":["Hi"],"score":100.0}]}
		answers = r.json()
		if( "answers" in answers ):
			self.answers = answers["answers"] # Extract list of QnA dictionaries
			self.answerIndex = 0 
			return r.status_code
		else:
			print "!ERROR!"
			print r.text
			return 0 

	# Returns list of QnA dictionaries
	def GetAnswerList(self):
		return self.answers

	# Returns next QnA dictionary in list
	# Use qnaDict["answer"] to get answer string, qnaDict["score"] to get numeric score
	def GetNextAnswer(self):
		if( self.answerIndex < len(self.answers) ):
			qnaDict = self.answers[self.answerIndex]
			self.answerIndex += 1
			return qnaDict

		return None
