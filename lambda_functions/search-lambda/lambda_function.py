import json
import boto3
import requests
from inflect import inflect

client = boto3.client('lex-runtime')

def lambda_handler(event, context):

    message = event['q']
        
    #message = "images of dog and cat"
    response = client.post_text(
            botName="SearchPhotos",
            botAlias='$LATEST',
            userId="random",
            sessionAttributes={ },
            requestAttributes={ },
            inputText = message,
        )
    print(response)
    
    if 'slots' in response.keys():
        slot_infos = response['slots']
        
        
        if p.singular_noun(slot_infos['label_type_one']) == False:
            slot_1 = slot_infos['label_type_one']
        else: 
            slot_1 = p.singular_noun(slot_infos['label_type_one']) if slot_infos['label_type_one'] is not None else ""
        
        if slot_infos['label_type_two'] is not None:
            if p.singular_noun(slot_infos['label_type_two']) == False:
                slot_2 = slot_infos['label_type_two']
            else: 
                slot_2 = p.singular_noun(slot_infos['label_type_two']) if slot_infos['label_type_two'] is not None else ""
        else:
            slot_2 = ""

        detected_slots = slot_1 + slot_2
    else:
        detected_slots = msg
        
    print("Detected slots:", detected_slots)
    
    # slot_infos = response['slots']
    # #print(slot_infos)
    # slot_1 = slot_infos['label_type_one'] if slot_infos['label_type_one'] is not None else ""
    # slot_2 = slot_infos['label_type_two'] if slot_infos['label_type_two'] is not None else ""
    
    # detected_slots = slot_1 + " " + slot_2
    # print(detected_slots)
    
    headers = {'Content-Type' : 'application/json'}
    ENDPOINT = "https://search-photos-ln6kglcspndf5qvmzygoqel7sa.us-east-1.es.amazonaws.com/photos"
    url = ENDPOINT + '/_search?size=1&&q=labels:' +  detected_slots
    
    response = requests.get(url, headers=headers, auth=("Administrator", "admin@AWS123")).json()

    es_responses = response['hits']['hits']
    image_list = ["https://b2-hw2.s3.amazonaws.com/" + img_object['_source']['objectKey'] for img_object in es_responses]
    
    print(image_list)
    
    return {
        'statusCode': 200,
        'body': image_list
    }
