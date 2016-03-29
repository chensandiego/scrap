from bs4 import BeautifulSoup
import requests
import json
import threading


#SO_URL = "http://scifi.stackexchange.com"

SO_URL = "http://stackoverflow.com"

QUESTION_LIST_URL = SO_URL +"/questions"

MAX_PAGE_COUNT=20


class ThreadManager:
	instance = None
	final_results =[]
	threads_done = 0
	totalConnections = 4

	@staticmethod
	def notify_connection_end(partial_results):
		print ("=======Thread is done!==========")
		ThreadManager.threads_done +=1
		ThreadManager.final_results +=partial_results
		if ThreadManager.threads_done == ThreadManager.totalConnections:
			print("==========saving data to file!=========")
			with open('scrapping-results-optimized.json','w') as outfile:
				json.dump(ThreadManager.final_results,outfile,indent=4)




global_results = []

initial_page =1 #first page is page 1
def get_author_name(body):
	link_name=body.select(".user-details a")
	if len(link_name)==0:
		text_name = body.select(".user-details")
		return text_name[0].text if len(text_name)>0 else 'N/A'
	else:
		return link_name[0].text

def get_question_answers(body):
	answers = body.select(".answer")
	a_data=[]
	if len(answers) ==0:
		return a_data 

	for a in answers:
		data = {
			'body':a.select(".post-text")[0].get_text(),
			'author':get_author_name(a)
		}
		a_data.append(data)
	return a_data 

def get_question_data(url):
	print ("Getting data from question page:%s" %(url))
	resp=requests.get(url)
	if resp.status_code!=200:
		print ("error while trying to scrape url:%s"%(url))
		return
	body_soup= BeautifulSoup(resp.text)
	#define the output dict that will be turned into a JSON 
	q_data={
		'title':body_soup.select('#question-header .question-hyperlink')[0].text,
		'body':body_soup.select('#question .post-text')[0].get_text(),
		'author':get_author_name(body_soup.select(".post-signature.owner")[0]),
		'answers':get_question_answers(body_soup)

	}
	return q_data


def get_questions_page(page_num,end_page,partial_results):
	print ("=======================================")
	print ("Getting list of questions for page %s" %(page_num))
	print ("=======================================")

	url=QUESTION_LIST_URL + "?sort=newest&page=" + str(page_num)
	resp = requests.get(url)
	if resp.status_code !=200:
		print ("Error while trying to scrape url:%s" %(url))
	else:
		body = resp.text 
		main_soup = BeautifulSoup(body)

		#get url for each question
		questions = main_soup.select('.question-summary .question-hyperlink')
		urls = [SO_URL + x['href'] for x in questions]
		for url in urls:
			q_data = get_question_data(url)
			partial_results.append(q_data)
	
	if page_num +1 < end_page:
		get_questions_page(page_num +1,end_page,partial_results)
	else:
		ThreadManager.notify_connection_end(partial_results)


pages_per_connection=MAX_PAGE_COUNT/ThreadManager.totalConnections


for i in range(ThreadManager.totalConnections):
	init_page = i * pages_per_connection
	end_page=init_page+pages_per_connection
	t= threading.Thread(target=get_questions_page,args=(init_page,end_page,[],),name='connection-%s'%(i))
	t.start()