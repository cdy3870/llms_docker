import string
import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
import requests
import plotly.express as px

st.set_page_config(
	page_title="Conference Recommender", layout="wide")

st.markdown(
	"""
<style>
[data-testid="stMetricValue"] {
	font-size: 20px;
}
</style>
""",
	unsafe_allow_html=True,
)

def generate_url(paper):
	URL = "https://arxiv.org/search/?query="
	for string in paper.split(" "):
		URL = URL + string + "+"
	URL = URL[:-1]
	URL += "&searchtype=all&source=header"
	return URL

def generate_conf_url(conf):
	URL = "https://www.scimagojr.com/journalsearch.php?q="
	print(conf.split(" "))
	for string in conf.split(" "):
		URL = URL + string + "+"
	URL = URL[:-1]
	return URL

def find_year(raw_data):
	mapping = {}
	max_value = 0
	for text in raw_data:
		table = str.maketrans(dict.fromkeys(string.punctuation))
		parsed_text = text[0].translate(table)   
		for word in parsed_text.split(" "):
			if word.isdigit():
				mapping[int(word)] = text[1]
				if int(word) > max_value:
					max_value = int(word)
				break
	if max_value == 0:
		return raw_data[0][1]
				
	return mapping, max_value

def get_h5_index(URL):
	r = requests.get(URL)
	soup = BeautifulSoup(r.content,  "html.parser")
	raw_data = []
	for a in soup.find_all('a', href=True):
		if "journalsearch" in a["href"]:
			raw_data.append([a.span.text, a["href"]])

	mapping, max_value = find_year(raw_data)
	url = "https://www.scimagojr.com/" + mapping[max_value]
	r = requests.get(url)
	soup = BeautifulSoup(r.content,  "html.parser")
	html = soup.find(class_ = "hindexnumber")
	return html.text

def parse_recs(recs):
	papers = recs.split("\n")
	papers = [p[3:] for i, p in enumerate(papers) if i != 0]
	return papers

def extract_id(URL):
	r = requests.get(URL)
	soup = BeautifulSoup(r.content,  "html.parser")
	
	id = soup.find(class_ = "list-title is-inline-block").text[6:16]
	return id

def extract_conference(id): 
	URL = f"https://arxiv.org/abs/{id}"
	r = requests.get(URL)
	soup = BeautifulSoup(r.content,  "html.parser")
	html = soup.find(class_ = "tablecell comments mathjax")
	# html = soup.find(class_ = "arxivid")
	if html:
		conf = html.text
	else:
		conf = "No conference found in arxiv"
	return conf

def find_year(raw_data):
	mapping = {}
	max_value = 0
	for text in raw_data:
		table = str.maketrans(dict.fromkeys(string.punctuation))
		parsed_text = text[0].translate(table)   
		for word in parsed_text.split(" "):
			if word.isdigit():
				mapping[int(word)] = text[1]
				if int(word) > max_value:
					max_value = int(word)
				break
	if max_value == 0:
		return raw_data[0][1]
				
	return mapping, max_value

def generate_prompt(conf):
	# prompt = "Can you extract the only conference from these strings: " 
	# for conf in confs:
	#     prompt = prompt + f"\'{conf}\'" + ", "
	# prompt = prompt[:-2]
	
	# prompt += " without the date, any form of abbreviation, or workshop"

	few_shot_prompt = f"Extract the main conference from the corresponding texts below without any numbers or abbreviations. \n\
	Text 1: Proceedings of the 46th ACM Symposium on Theory of Computing (STOC 2014), pp. 283-292 (2014) \n\
	Conference 1: Symposium on Theory of Computing \n\n\
	Text 2: The paper has been accepted by IEEE Transactions on Cognitive Communications and Networking \n\
	Conference 2: Transactions on Cognitive Communications and Networking \n\n\
	Text 3: Accepted by the ACM Transactions on Intelligent Systems and Technology (TIST) \n\
	Conference 3: Transactions on Intelligent Systems and Technology \n\n\
	Text 4: Proceedings of the Interdisciplinary Workshop on Human-Drone Interaction co-located with the 2020 ACM CHI Conference on Human Factors in Computing Systems (CHI 2020) - this http URL \n\
	Conference 4: Conference on Human Factors in Computing Systems \n\n\
	Text 5: {conf} \n\
	Conference 5: "
	
	return few_shot_prompt




def make_df(papers, confs, h5_indices):
	# conf = ["test", "test", "test"]
	sample_impact = [5, 8, 6]
	
	chart = pd.DataFrame({"Conference": confs, "Related Paper": papers, "Most Recent H5-index": h5_indices, "Impact Score": sample_impact})
	# chart["Publish Date"] = pd.to_datetime(chart["Publish Date"])
	chart_1 = chart.sort_values("Most Recent H5-index", ascending=False)
	# chart_2 = chart.sort_values("Impact Score", ascending=False)
	bar_chart = px.bar(chart, x="Most Recent H5-index", y="Conference", orientation="h")

	return chart_1, bar_chart



st.markdown("<h1 style='text-align: center'> Conference Recommendation for Your Research </h1>", unsafe_allow_html=True)



doi = st.text_input("Enter a description about your paper")
inputs = {"text": doi}

if st.button("Get similar papers"):
	# res = requests.post(url="http://0.0.0.0:8000/get_recs", json=inputs)
	# recs = res.text
	# papers = parse_recs(recs)
	papers = ['Human-Drone Interactions with Semi-Autonomous Cohorts of Collaborating Drones',
 'Sound-based drone fault classification using multitask learning',
 'Post-disaster 4G/5G Network Rehabilitation using Drones: Solving Battery and Backhaul Issues']
	URLs = [generate_url(paper) for paper in papers]
	ids = [extract_id(url) for url in URLs]
	confs = [extract_conference(id) for id in ids]

	parsed_confs = []

	for conf in [confs[0]]:
		prompt = generate_prompt(conf)
		inputs = {"text": prompt}
		# res = requests.post(url="http://0.0.0.0:8000/get_main_confs", json=inputs)
		# print(res.text)
		# parsed_confs.append(res.text)
	
	parsed_confs = [s.strip() for s in ["International Congress on Sound and Vibration",
					"International Conference on Service Oriented Computing",
					"Conference on Human Factors in Computing Systems"]]


	h5_indices = []
	for parsed_conf in parsed_confs:
		conf_url = generate_conf_url(parsed_conf)
		h5_index = get_h5_index(conf_url)
		h5_indices.append(int(h5_index))

	chart_1, bar_chart = make_df(papers, parsed_confs, h5_indices)
	st.markdown("Recommended Conference Based on Related Papers and H5-index")
	st.dataframe(chart_1[["Conference", "Related Paper"]])
	st.plotly_chart(bar_chart)



#drone type classification using time series data