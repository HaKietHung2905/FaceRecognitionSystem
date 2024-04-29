from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
import os
import functions.readConfig as readConfig
#import readConfig as readConfig
import mysql.connector  
import numpy as np
import pandas as pd
import json 
import math
from deepface import DeepFace
from deepface.commons import package_utils, folder_utils

os.environ['OPENAI_API_KEY'] = "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"



#response = chain.invoke({"input": "Give me image with happy emotion, age arround 30 in, male and white guy?"})



def get_images_data(database_name, select_statement, type):
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
    
    results = cursor.execute(select_statement)

    datas  = cursor.fetchall()  # Fetch all rows
    db_connection.commit()

    instances = []
    if type == 1:
        for data in datas:
            img_name = data[0]
            embedding_bytes = data[1]

            # Decode JSON string to Python object
            embedding_list = json.loads(data[1])
        
            # Convert the list to a NumPy array
            embedding = np.array(embedding_list, dtype=np.float32)
        
            
            instance = []
            instance.append(img_name)
            instance.append(embedding)
            instances.append(instance)
    else: 
        for data in datas:
            img_name = data[0]
            distance_squared = data[1]
            
            instance = []
            instance.append(img_name)
            instance.append(math.sqrt(distance_squared))
            instances.append(instance)
    #print(instances)    
    
    cursor.close()
    db_connection.close()

    return instances

def find_euclidean_distance(row):
    source = np.array(row['embedding'])
    target = np.array(row['target'])
    distance = (source - target)
    return np.sqrt(np.sum(np.multiply(distance, distance)))

def prediction_images(image_path):
    target_embedding = DeepFace.represent(img_path = image_path, model_name = "Facenet", enforce_detection= False)[0]["embedding"]

    
    # Get the data from the database

    select_statement = "select img_name, embedding from face_meta"
    instances = get_images_data('database', select_statement, 1)
    result_df = pd.DataFrame(instances, columns = ["img_name", "embedding"])

    # Add the target embedding to the dataframe
    my_list = [target_embedding,]
    target_duplicated = np.array(my_list*result_df.shape[0])
    result_df['target'] = target_duplicated.tolist()

    result_df['distance'] = result_df.apply(find_euclidean_distance, axis = 1)
    result_df = result_df[result_df['distance'] <= 10]
    result_df = result_df.sort_values(by = ['distance']).reset_index(drop = True)
    result_df = result_df.drop(columns = ["embedding", "target"])


    target_statement = ""
    for i, value in enumerate(target_embedding):
        target_statement += "select %d as dimension, %s as value" % (i, str(value)) #sqlite
        #target_statement += "select %d as dimension, %s as value from dual" % (i, str(value)) #oracle
        
        if i < len(target_embedding) - 1:
            target_statement += " union all "
    
    select_statement = f"""
      SELECT * 
        FROM (
            SELECT img_name, SUM(subtract_dims) AS distance_squared
            FROM (
                SELECT img_name, (source - target) * (source - target) AS subtract_dims
                FROM (
                    SELECT meta.img_name, emb.value AS source, target.value AS target
                    FROM face_meta meta 
                    LEFT JOIN face_embeddings emb ON meta.id = emb.face_id
                    LEFT JOIN (
                        {target_statement}
                    ) target ON emb.dimension = target.dimension
                ) AS subquery
            ) AS inner_subquery
            GROUP BY img_name
        ) AS outer_subquery
        WHERE distance_squared < 100
        ORDER BY distance_squared ASC;
        """
    
    print ('Select statement:', select_statement)
    instances = get_images_data('database', select_statement, 2)   

    result_df = pd.DataFrame(instances, columns = ["img_name", "distance"])
    result_list = result_df.to_dict(orient='records')
    #print(result_list)
    return result_list
    #return select_statement
 


# Example usage

#image_path = "../static/queryImages/img67.jpg"
#query_input = "SELECT img_name, dominant_emotion, age, dominant_gender, dominant_race FROM face_meta WHERE dominant_emotion = 'neutral' AND age BETWEEN 28 AND 38 AND dominant_gender = 'man' AND dominant_race = 'white';"
#result = predictionImages(image_path)
