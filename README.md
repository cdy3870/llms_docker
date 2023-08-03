# Research Conference Recommender

This repo contains the code that for the research conference recommender. The purpose is to remove the hassle of figuring out which research conference you should submit your work to. 

## Requirements

The "frontend" is done using Streamlit and the backend/REST API is FastAPI. The setup has been simplified using Docker with multiple containers. The containers with be running on an AWS EC2 
instance. Follow the below instructions in the case that the servers are no longer running on AWS.

```
cd llms_docker
docker-compose up
```

Otherwise, you can access the service here: (under maintainence)

## Libraries, Frameworks, APIs, Cloud Services
1. Libraries and Frameworks
- FastAPI
- Streamlit
- Docker
- BeautifulSoup
2. APIs
- OpenAI
- arXiv
- Serper

## How it works and services involved
1. LangChain is a library used to leverage the capabilities of large language models (llms), when OpenAI's llm is paired with a tool, it is capable of reasoning beyond the environment it was 
trained in
- When paired with the arXiv API, an agent can be created to query and reason with research paper database
- We make a request for papers related to a specific research topic
2. Once we parse the recommended papers, we can extract the arXiv ids by using a web scraping tool called BeautifulSoup
3. After obtaining arXiv ids, we can find the corresponding conference within the page as well
4. The last step is to use the Serper API to create another agent that can figure out the H5-index and impact score of the conference
- More about those metrics (https://libguides.wakehealth.edu/researchmetrics/journal#:~:text=H5%2Dindex%20%22It%20is%20the,60%20or%20more%20citations%20each)
5. We make our final suggestions based on these metrics



