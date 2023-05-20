import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
# from ksuid import ksuid


db = boto3.resource('dynamodb')
table = db.Table('papel_student_table')

studentPath = "/students" 

def lambda_handler(event, context):
    if event['path'] == studentPath:
        if event['httpMethod'] == "GET":
            if event['queryStringParameters'] is not None:
                sid = event['queryStringParameters']['id']
                if sid is not None:                   
                    response = table.get_item(
                        Key={
                            'id': sid
                        }
                    )                 
                    return {
                        "statusCode": 200,
                        # 'headers': {
                        #     'Access-Control-Allow-Headers': 'Content-Type',
                        #     'Access-Control-Allow-Origin': '*',
                        #     'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                        # },
                        "body": json.dumps(response['Item'])
                    }                  
            else:          
                response = table.scan()['Items']           
                return {
                    "statusCode": 200,
                    # 'headers': {
                    #     'Access-Control-Allow-Headers': 'Content-Type',
                    #     'Access-Control-Allow-Origin': '*',
                    #     'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    # },
                    "body": json.dumps(response)
                }    
        elif event['httpMethod'] == "POST":
            b = json.loads(event['body'])
            s_id = b['id']
            s_name = b['full_name']
            s_subj = b['subject']
            # ks = "#1234"
            # sks = str(ks)
            insert_data = {               
                'id': s_id,
                'full_name': s_name,
                'subject': s_subj,
            }
            try:
                table.put_item(Item=insert_data)
                return {
                    'statusCode': 201,
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },
                    'body': json.dumps({"message":"Student added successfully!!"})
                }
            except ClientError as e:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },
                    'body': json.dumps({"message": str(e.response['Error'])})
                }
        
        elif event['httpMethod'] == "PATCH":            
            requestBody = json.loads(event['body'])   
            studentId = requestBody['id']    
            # for key,val in requestBody.items():  
            s_name = requestBody['full_name']
            s_subj = requestBody['subject']
            try:               
                table.update_item(
                    Key = {'id':studentId},
                    UpdateExpression="set full_name = :a, subject = :b", 
                    ExpressionAttributeValues={
                            ':a': s_name,
                            ':b': s_subj
                        },
                    ReturnValues='UPDATED_NEW'
                )
            except ClientError as e:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },
                    'body': json.dumps({"message": str(e.response['Error'])})
                }
            
            return {
                'statusCode': 201,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps({"message":"Student updated successfully!!"})
            }
                

            # name = b['name']           
            # subject = b['subject']
            
        # elif event['httpMethod'] == "DELETE":
            # key = {'PK': event['pathParameters']['id'],'SK':event['pathParameters']['id']}
            # b = json.loads(event['body'])
            # pk = b['id']
            # key = {'PK': pk,'SK':pk}
            # response = table.delete_item(Key=key)
            # return {
            #     "statusCode": 200,
            #     'headers': {
            #         'Access-Control-Allow-Headers': 'Content-Type',
            #         'Access-Control-Allow-Origin': '*',
            #         'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            #     },
            #     "body": json.dumps({'message':'Category deleted successfully'})
            # }
        
    else:       
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Invalid route!",
                # "location": ip.text.replace("\n", "")
            }),
        }