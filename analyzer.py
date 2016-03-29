import operator
import string
import nltk
from nltk.util import ngrams
import json
import re
import visualizer


SOURCE_FILE = './scrapping-results-optimized.json'


#load the json
def load_json_data(file):
	with open(file)as input_file:
		return json.load(input_file)


def analyze_data(d):
	return {
		'shortest_answer':get_shortest_answer(d),
		'most_active_users':get_most_active_users(d,10),
		'most_active_topics':get_most_active_topics(d,10),
		'most_helpful_user':get_most_helpful_user(d,10),
		'most_answered_questions':get_most_answered_questions(d,10),
		'most_common_phrases':get_most_common_phrases(d,10,4),

	}

def flatten_questions_body(data):
	body=[]
	for q in data:
		body.append(q['body'])
	return '.'.join(body)


def flatten_questions_titles(data):
	body=[]
	pattern = re.compile('(\[|\])')
	for q in data:
		lowered = q['title'].lower()
		filtered = re.sub(pattern,'',lowered)
		body.append(filtered)
	return '.'.join(body)


def get_most_active_users(data,limit):
	names = {}
	for q in data:
		if q['author'] not in names:
			names[q['author']]=1
		else:
			names[q['author']]+=1
	return sorted(names.items(),reverse=True,key=operator.itemgetter(1))[:limit]

def get_node_content(node):
	return ' '.join([x[0] for x in node])


def get_most_active_topics(data,limit):
	body = flatten_questions_titles(data)
	sentences = nltk.sent_tokenize(body)
	sentences = [nltk.word_tokenize(sent) for sent in sentences]
	sentences = [nltk.pos_tag(sent) for sent in sentences]
	grammar = "NP: {<JJ>?<NN.*>}"
	cp = nltk.RegexpParser(grammar)
	results={}
	for sent in sentences:
		parsed = cp.parse(sent)
		trees = parsed.subtrees(filter=lambda x: x.label()=='NP')
		for t in trees:
			key = get_node_content(t)
			if key in results:
				results[key]+=1
			else:
				results[key]=1
	return sorted(results.items(),reverse=True,key=operator.itemgetter(1))[:limit]


def get_most_helpful_user(data,limit):
	helpful_users={}
	for q in data:
		for a in q['answers']:
			if a['author'] not in helpful_users:
				helpful_users[a['author']]=1
			else:
				helpful_users[a['author']] +=1
	return sorted(helpful_users.items(),reverse=True,key=operator.itemgetter(1))[:limit]

def get_most_answered_questions(d,limit):
	questions = {}
	for q in d:
		questions[q['title']]=len(q['answers'])
	return sorted(questions.items(),reverse=True,key=operator.itemgetter(1))[:limit]

def get_most_common_phrases(d,limit,length):
	body=flatten_questions_body(d)
	phrases={}
	for sentence in nltk.sent_tokenize(body):
		words = nltk.word_tokenize(sentence)
		for phrase in ngrams(words,length):
			if all(word not in string.punctuation for word in phrase):
				key = ' '.join(phrase)
				if key in phrases:
					phrases[key]+=1
				else:
					phrases[key]=1
	return sorted(phrases.items(),reverse=True,key=operator.itemgetter(1))[:limit]

def get_shortest_answer(d):
	shortest_answer={
		'body':'',
		'length':-1
	}
	for q in d:
		for a in q['answers']:
			if len(a['body'])<shortest_answer['length'] or shortest_answer['length']==-1:
				shortest_answer={
					'question':q['body'],
					'body':a['body'],
					'length':len(a['body'])
				}
	return shortest_answer




data_dict = load_json_data(SOURCE_FILE)
results = analyze_data(data_dict)

print ("===(shortest answer)=========")
visualizer.displayShortestAnswer(results['shortest_answer'])

print ("===(most active users)=========")
visualizer.displayMostActiveUsers(results['most_active_users'])

print ("===(Most active topics)=========")
visualizer.displayMostActiveTopics(results['most_active_topics'])

print ("===(Most helpful users)=========")
visualizer.displayMostHelpfulUsers(results['most_helpful_user'])

print ("===(Most Answered questions)=========")
visualizer.displayMostAnsweredQuestions(results['most_answered_questions'])

print ("===(Most Common Phrases)=========")
visualizer.displayMostCommonPhrases(results['most_common_phrases'])



