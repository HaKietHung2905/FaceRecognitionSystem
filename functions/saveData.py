import mysql.connector  
import configparser
import json
from deepface import DeepFace
from deepface.commons import package_utils, folder_utils
import os

from datetime import datetime
import hashlib


def detect_images(PATH):
    model = DeepFace.build_model("Facenet")
    print(PATH)
    instances = [] 

    embedding = DeepFace.represent(img_path=PATH, model_name="Facenet", enforce_detection=False)[0]["embedding"]
    objs = DeepFace.analyze(img_path=PATH) 
    instance = {}
    instance["img_name"] = os.path.basename(PATH)
    instance["embedding"] = embedding
    instance["age"] = objs[0]["age"]
    instance["dominant_emotion"] = objs[0]["dominant_emotion"]
    instance["dominant_gender"] = objs[0]["dominant_gender"]
    instance["dominant_race"] = objs[0]["dominant_race"]
    #print(instance)
    
    return instance

def read_config(database_name):
    config = configparser.ConfigParser()
    #config.read('../config.ini')
    config.read('config.ini')
    return config[database_name]

# Function to connect to and insert data into the database
def connect_database(database_name, instance):

    config_data = read_config(database_name)
    print(config_data)
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

    img_name = instance["img_name"]
    embeddings = instance["embedding"]
    age = instance["age"]
    dominant_emotion = instance["dominant_emotion"]
    dominant_gender = instance["dominant_gender"]
    dominant_race = instance["dominant_race"]
     
    # Convert embeddings to JSON string
    embeddings_json = json.dumps(embeddings)
    
    # Insert into face_meta table
    current_time = datetime.now()
    unique_key = hashlib.sha256(str(current_time).encode()).hexdigest()


    insert_statement = "INSERT INTO face_meta (ID, IMG_NAME, EMBEDDING, AGE, DOMINANT_EMOTION, DOMINANT_GENDER, DOMINANT_RACE) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    insert_args = (unique_key, img_name, embeddings_json, age, dominant_emotion, dominant_gender, dominant_race)

    cursor.execute(insert_statement, insert_args)

    # Insert into face_embeddings table
    for i, embedding in enumerate(embeddings):
        insert_statement = "INSERT INTO face_embeddings (FACE_ID, DIMENSION, VALUE) VALUES (%s, %s, %s)"
        insert_args = (unique_key,i, embedding)
        cursor.execute(insert_statement, insert_args)

    db_connection.commit()

    cursor.close()
    db_connection.close()

#Sample Usage
if __name__ == "__main__":
    # Specify the path to the image you want to process
    image_path = "../test_dataset/img58.jpg"
    
    # Detect information from the image
    instance = detect_images(image_path)
    
    # Connect to the database and insert the detected information
    connect_database('database', instance)
