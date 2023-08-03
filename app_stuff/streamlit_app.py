import streamlit as st
import requests
import json
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests

st.set_page_config(
	page_title="Conference Recommender", layout="wide")


def generate_url(paper):
    URL = "https://arxiv.org/search/?query="
    for string in paper.split(" "):
        URL = URL + string + "+"
    URL = URL[:-1]
    URL += "&searchtype=all&source=header"
    return URL

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

# def parse_conf(conf):
# 	return None

# def parse_h5(h5):
# 	return None

# def parse_impact(impact):
# 	return None


def make_df(papers, confs):
	# conf = ["test", "test", "test"]
	sample_h5 = [53, 34, 23]
	sample_impact = [5, 8, 6]
	chart = pd.DataFrame({"Conference": confs, "Related Paper": papers, "H5-index": sample_h5, "Impact Score": sample_impact})
	# chart["Publish Date"] = pd.to_datetime(chart["Publish Date"])
	chart_1 = chart.sort_values("H5-index", ascending=False)
	chart_2 = chart.sort_values("Impact Score", ascending=False)

	return chart_1, chart_2



st.markdown("<h1 style='text-align: center'> Conference Recommendation for Your Research </h1>", unsafe_allow_html=True)



doi = st.text_input("Enter a description about your paper")
inputs = {"text": doi}

if st.button("Get similar papers"):
	# res = requests.post(url="http://0.0.0.0:8000/get_recs", json=inputs)
	# recs = res.text

	recs = "There are three papers about 'drone type classification using time series data' which have been accepted into a conference: \n1. Sound-based drone fault classification using multitask learning\n2. Constraint-Aware Trajectory for Drone Delivery Services\n3. Fast and Accurate Time Series Classification with WEASEL"
	papers = parse_recs(recs)
	URLs = [generate_url(paper) for paper in papers]
	ids = [extract_id(url) for url in URLs]
	confs = [extract_conference(id) for id in ids]

	chart_1, chart_2 = make_df(papers, confs)
	st.markdown("Recommended Conference Based on H5-index")
	st.dataframe(chart_1)
	st.markdown("Recommended Conference Based on Impact Score")
	st.dataframe(chart_2)




#drone type classification using time series data


# text_input = st.text_input("Enter some text")
# cand_labels = st.text_input("Candidate labels")


# # Get a prediction
# # sequence_to_classify = "one day I will see the world"
# # candidate_labels = ['travel', 'cooking', 'dancing']
# # labels = cand_labels.split(" ")

# inputs = {"text_input": text_input, "candidate_labels": cand_labels}

# if st.button("Get most likely label"):
# 	res = requests.post(url="http://0.0.0.0:8000/predict_sentiment", json=inputs)
# 	predictions = json.loads(res.text)
# 	sequence = predictions["labels"][np.argmax(predictions["scores"])]

# 	st.subheader(f"{sequence}")