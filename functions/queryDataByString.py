from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
import os
import functions.readConfig as readConfig
import mysql.connector  
#import readConfig as readConfig

os.environ['OPENAI_API_KEY'] = "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"



#response = chain.invoke({"input": "Give me image with happy emotion, age arround 30 in, male and white guy?"})


def get_sql_query(input_string):
    #os.environ['OPENAI_API_KEY'] = "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"

    embeddings = OpenAIEmbeddings()
    output_parser = StrOutputParser()
    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are mySQL expert, convert input string to only SELECT top 15 statement with extraction of img_name, dominant_emotion, age, dominant_gender, dominant_race from table face_meta. quey for gender will have 2 variable: man and woman. Answer SQL query only."),
        ("user", input_string)
    ])

    chain = prompt | llm | output_parser

    response = chain.invoke({"input": input_string})
    
    return response

def get_images_data(database_name, query_input):
    config_data = readConfig.read_config(database_name)
    host = config_data['server']
    database = config_data['database']
    username = config_data['username']
    password = config_data['password']

    # Connect to MySQL database
    db_connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )

    cursor = db_connection.cursor()

    # Insert into face_meta table
    
    cursor = db_connection.cursor()
    cursor.execute(query_input)
    result = cursor.fetchall()  # Fetch all rows
    db_connection.commit()

    print(result)    
    

    cursor.close()
    db_connection.close()

    return result

# Example usage
#database_name = "database"
#query_input = "SELECT img_name, dominant_emotion, age, dominant_gender, dominant_race FROM face_meta WHERE dominant_emotion = 'neutral' AND age BETWEEN 28 AND 38 AND dominant_gender = 'man' AND dominant_race = 'white';"
#result = get_images_data(database_name, query_inpu)

#print(result)