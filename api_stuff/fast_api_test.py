from typing import List
from fastapi import FastAPI, Query
from joblib import load
from pydantic import BaseModel
from transformers import pipeline
import json
import os
from langchain.llms import OpenAI
from langchain.agents import load_tools, initialize_agent, AgentType, Tool
import openai
import pickle
import pandas as pd

all_main_categories = ['Agricultural and Biological Sciences',
 'Arts and Humanities',
 'Biochemistry, Genetics and Molecular Biology',
 'Business, Management and Accounting',
 'Chemical Engineering',
 'Chemistry',
 'Computer Science',
 'Decision Sciences',
 'Dentistry',
 'Earth and Planetary Sciences',
 'Economics, Econometrics and Finance',
 'Energy',
 'Engineering',
 'Environmental Science',
 'Health Professions',
 'Immunology and Microbiology',
 'Materials Science',
 'Mathematics',
 'Medicine',
 'Multidisciplinary',
 'Neuroscience',
 'Nursing',
 'Pharmacology, Toxicology and Pharmaceutics',
 'Physics and Astronomy',
 'Psychology',
 'Social Sciences',
 'Veterinary']

classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")
# api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = api_key
# llm = OpenAI()
# arxiv_tools = load_tools(["arxiv"])
# arxiv_agent = initialize_agent(arxiv_tools, llm, 
# 								agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

new_mapping = pd.read_pickle("mapping.pkl")

# Initialize an instance of FastAPI
app = FastAPI()

def get_predictions(topic, all_main_categories):
	# dropped = all_main_categories.drop("Multidisciplinary")
    results = classifier(topic,
        candidate_labels=all_main_categories,
    )    
    return results["labels"], results["scores"]

def get_categories(main_categories):
	all_categories = []

	for q in main_categories:
		if q != "Multidisciplinary":
			all_categories += new_mapping[q]

	return all_categories

class Item(BaseModel):
    text: str

# class ListItem(BaseModel):
# 	text: str
# 	list_items: List[str]
    
@app.get("/")
def root():
	return {"message": "arXiv backend"}

@app.post("/get_recs")
def get_recs(topic: Item):
	response = arxiv_agent.run(f"Can you find a list of papers about {topic.text} and have been accepted into a conference as bullet points?")
	# print(response)

	return response

@app.post("/get_main_confs")
def get_main_confs(prompt: Item):
	response = openai.Completion.create(engine="text-davinci-003", prompt=prompt.text, max_tokens=100,stop=None,temperature=0.7)["choices"][0]["text"]
	return response


@app.post("/get_main_cat_preds")
def get_main_cat_preds(topic: Item):
	top_labels, top_scores = get_predictions(topic.text, all_main_categories)
	response = json.dumps(dict(zip(top_labels, top_scores)))
	return response

# @app.post("/get_cat_preds")
# def get_main_cat_preds(info: ListItem):
# 	all_categories = new_mapping[info.list]
# 	top_labels, top_scores = get_predictions(info.text, all_main_categories)
# 	response = json.dumps(dict(zip(top_labels, top_scores)))
# 	return response


@app.get("/get_cat_preds")
def get_cat_preds(query: List[str] = Query(...)):
	all_categories = get_categories(query[1:])
	top_labels, top_scores = get_predictions(query[0], all_categories)
	response = json.dumps(dict(zip(top_labels, top_scores)))
	return response

