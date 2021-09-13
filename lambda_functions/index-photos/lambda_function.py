import json
import boto3
import datetime 
import requests
import base64


def lambda_handler(event, context):
    # TODO implement
    
    print("My code ran successfully!")

    client = boto3.client("rekognition")
    s3 = boto3.client("s3")
    
    record = event['Records'][0]
    print(record)
    
    image_key = record['s3']['object']['key']
    bucket_name = record['s3']['bucket']['name']
    response_elements = record['responseElements']
    #meta_fields = s3.head_object(Bucket=bucket_name, Key=image_key)
    
    print("Image ", image_key, "Bucket Name: ", bucket_name)
    
    # Get image    
    #fileObj = s3.get_object(Bucket = bucket_name, Key=image_key)
    #print("-----------------fileObj-----------------------", fileObj)
    #file_content = fileObj["Body"].read()
    #base_64_image = base64.b64decode(file_content)
    recognition_response = client.detect_labels(Image = {'S3Object': {'Bucket': bucket_name, 'Name': image_key}}, MaxLabels=5, MinConfidence=70) 
    
    #recognition_response = client.detect_labels(Image = {'Bytes': base_64_image}, MaxLabels=5, MinConfidence=70) 
    
    print(recognition_response)
    #print(recognition_response)
    
    # get labels
    
    label_list = recognition_response['Labels']
    labels = [element['Name'] for element in label_list]
    
    print(labels)
    object_json = {
        "objectKey": image_key,
        "bucket": bucket_name,
        "labels" : labels,
        "createdTimeStamp": datetime.datetime.now().isoformat()
    }
    
    print(object_json)
    
    headers = {'Content-Type' : 'application/json'}
    ENDPOINT = "https://search-photos-ln6kglcspndf5qvmzygoqel7sa.us-east-1.es.amazonaws.com/photos/photo/"
    url = ENDPOINT 
    
    response = requests.put(url + object_json["objectKey"], headers=headers, auth=("Administrator", "admin@AWS123"), json=object_json)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
