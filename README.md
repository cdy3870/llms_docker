# Research Conference Recommender

This repo contains the code that for the research conference recommender. The purpose is to remove the hassle of figuring out which research conference you should submit your work to. 

## Requirements

The "frontend" is done using Streamlit and the backend/REST API is FastAPI. The setup has been simplified using Docker with multiple containers. The containers will be running on an AWS EC2 
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
3. Resources
- https://www.scimagojr.com/ for conference metrics

## How it works and services involved
1. LangChain is a library used to leverage the capabilities of large language models (llms), when OpenAI's llm is paired with a tool, it is capable of reasoning beyond the environment it was 
trained in
- When paired with the arXiv API, an agent can be created to query and reason with a research paper database
- We make a request for papers related to a specific research topic
2. Once we parse the recommended papers, we can extract the arXiv ids by using a web scraping tool called BeautifulSoup
3. After obtaining arXiv ids, we can find the corresponding conference within the page as well
4. The issue with that the conference within the arXiv page is not processed so we may have a string like "Accepted by the ACM Transactions on Intelligent Systems and Technology (TIST)" but we only need "Transactions on Intelligent Systems and Technology" if we want to search correctly on the SJR conference website
- Therefore we use the DaVinci text completion engine to help parse out this conference
5. Then we can make the GET request on the SJR website
- The results may be multiple editions of the conference/journal, so we parse out all of them and get the most recent one
- The h5-index is then extracted 
6. We make our final suggestions based on these metrics



