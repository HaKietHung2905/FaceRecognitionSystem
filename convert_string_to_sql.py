from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
import os

os.environ['OPENAI_API_KEY'] = "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"


embeddings = OpenAIEmbeddings()
output_parser = StrOutputParser()
llm = ChatOpenAI()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are SQL expert, convert input string to only SELECT statement with extraction of img_name, dominant_emotion, age, dominant_gender, dominant_race"),
    ("user", "{input}")
])

chain = prompt | llm | output_parser

response = chain.invoke({"input": "Give me image of Messi with happy emotion, age arround 30 in, male and white guy?"})
print(response)

