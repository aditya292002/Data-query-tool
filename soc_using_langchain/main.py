from langchain_openai import AzureOpenAI
from langchain_experimental.agents import create_csv_agent

llm = AzureOpenAI(
    openai_api_key="91fa6d3ee64745dea59be9e2e21581f1", 
    deployment_name="gpt-35-turbo-instruct", 
    model_name="azure",
    api_version="2024-02-15-preview", 
    azure_endpoint="PLACE YOUR ENDPOINT HERE")

agent = create_csv_agent(llm = llm, path=['iam.csv', 'Firewall.csv'], verbose=True)
agent.invoke("How many rows of data do you have?")
agent.invoke("How many days of data do you have Nasdaq?")
agent.invoke("Was there any news which mentioned about some kind of stock drop?")
agent.invoke("Do you see any relation between potential stock drop and news and Nasdaq?")
agent.invoke("Was the drop of nasdaq index in 2012 related to the negative sentiment of the news?")
agent.invoke("In 2012, nasdaq index is growing or dropping?")


#keys
#(Key1: 91fa6d3ee64745dea59be9e2e21581f1 & Key2: f312a48c295f4c8c94094581b5ad7ba2
