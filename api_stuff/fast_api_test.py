from fastapi import FastAPI, HTTPException
from joblib import load
from pydantic import BaseModel
import json
import os
from langchain.llms import OpenAI
from langchain.agents import load_tools, initialize_agent, AgentType, Tool
import openai

llm = OpenAI()
arxiv_tools = load_tools(["arxiv"])
arxiv_agent = initialize_agent(arxiv_tools, llm,
								agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = 
api_key
# Initialize an instance of FastAPI
app = FastAPI()


# Define the default route 
@app.get("/")
def root():
	return {"message": "arXiv backend"}
	
class Item(BaseModel):
    text: str

@app.post("/get_recs")
def get_recs(topic: Item):
	response = arxiv_agent.run(f"Can you find a list of papers about {topic.text} and have been accepted into a conference as bullet points?")
	print(response)

	return response



@app.post("/get_main_confs")
def get_main_confs(prompt: Item):
	response = openai.Completion.create(engine="text-davinci-003", prompt=prompt.text, max_tokens=100,stop=None,temperature=0.7)["choices"][0]["text"]
	return response
