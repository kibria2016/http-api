import json

# from sam-tutorial.http-api.layers.python.test import LoginTest
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
# from ksuid import ksuid
# from config import *
import sys
sys.path.append('../')
from test import *
from pydantic import ValidationError
import os

USER_POOL_ID=os.environ.get("USER_POOL_ID")
# USER_POOL_ID="us-west-2_YAaIaRMeE"
USER_POOL_CLIENT_ID=os.environ.get("USER_POOL_CLIENT_ID")
# USER_POOL_CLIENT_ID="4oid31egmjossb8tsagkgim77p"

db = boto3.resource('dynamodb')
table = db.Table('papel_student_table')
# sns_client = boto3.client('sns', 'us-west-2')
client = boto3.client('cognito-idp', 'us-west-2')



def user_registration(event, context): 
    # b = json.loads(event['queryStringParameters'])
    # email = b['email']
    # password = b['password']
    email = None
    password = None
    for k,v in json.loads(event['body']).items():
        if k == 'email':
            email=v
        elif k == 'password':
            password=v    
    signup_response = []
    # addgroup_response = []
    msg = 'success!'
    try:
        signup_response = client.sign_up(
                ClientId=USER_POOL_CLIENT_ID,
                Username=email,
                Password=password,
                UserAttributes=[{'Name': 'email','Value': email}])
        print(signup_response)
    except ClientError as e:
        if e.response['Error']['Code'] == 'UsernameExistsException':
            # Todo Handle Already Exists Email
            msg="User already exists"
        if e.response['Error']['Code'] == 'ParamValidationError':
            # Todo Handle Param Validate
            msg="Param Validate Error"
        return {
            'statusCode': 201,
             'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({"msg":str(e.response['Error'])})
        } 
    

    # if msg == 'success!':
    #     userId = signup_response['UserSub']        
    #     try:
    #         # addgroup_response = client.admin_add_user_to_group(
    #         #     UserPoolId=USER_POOL_ID,
    #         #     Username=email,
    #         #     GroupName='Student'
    #         # ) 
    #         # insert = add_user_to_db(userId,email)
    #         # if insert ==  'insert success':
    #         #     msg='success!'
    #         #     print("db success!")           
    #         msg='success!'
    #     except ClientError as e:
    #         if e.response['Error']['Code'] == 'NotAuthorizedException':
    #             # Todo Handle Already Exists Email
    #             msg="Unauthorized"
    #         if e.response['Error']['Code'] == 'ParamValidationError':
    #             # Todo Handle Param Validate
    #             msg="Param Validate Error"
    #         if e.response['Error']['Code'] == 'UserNotFoundException':
    #             # Todo Handle Already Exists Email
    #             msg="User not found"    

    
    return {
            'statusCode': 201,
             'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({"msg":msg,"res":signup_response})
        } 


def signup_confirm(event, context):
    b = json.loads(event['body'])
    confirm_response = []
    msg = 'success!'
    try:
        confirm_response = client.confirm_sign_up(
            ClientId=USER_POOL_CLIENT_ID,
            Username=b['email'],
            ConfirmationCode=b['confirm_code']
            )
        print(confirm_response)    
    except ClientError as e:
        if e.response['Error']['Code'] == 'UserNotFoundException':
            # Todo Handle Already Exists Email
            msg="Can't Find user by Email"
        if e.response['Error']['Code'] == 'CodeMismatchException':
            # Todo Handle Param Validate
            msg="User Code Mismatch"
        if e.response['Error']['Code'] == 'ParamValidationError':
            # Todo Handle Param Validate
            msg="Param Validate Error"
        if e.response['Error']['Code'] == 'ExpiredCodeException':
            # Todo Handle Expired Code
           msg="Expired Code"
    return {
            'statusCode': 200,
            'headers': {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*"
            },
            'body': json.dumps({"msg":msg,"res":confirm_response}, default=str)
            # 'body': {"msg":msg}
        } 
    

def user_login(event, context):
    b = json.loads(event['body'])
    token = []
    msg = ""
    print(USER_POOL_CLIENT_ID)
    try:
        test = LoginTest(**b)
        auth_data = { 'USERNAME':test.email , 'PASSWORD':test.password }        
        resp = client.initiate_auth(
            ClientId=USER_POOL_CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH', 
            AuthParameters=auth_data
        )
        token = resp       
        msg = "Success!"       
    except client.exceptions.NotAuthorizedException:
        msg = "The username or password is incorrect"       
    except client.exceptions.UserNotConfirmedException:
        msg = "User is not confirmed"
    except client.exceptions.UserNotFoundException:
        msg = "User is not found"
    # except ClientError as e:
    #     msg = e.json()  
    #     msg = msg.replace('\n', '')    # do your cleanup here
    #     msg = json.loads(msg)
    #     data_len = len(msg)
       
    #     if data_len >1:
    #         if 'email' in msg[0]['loc'][0]:
    #             msg = "email required"
    #         elif 'password' in msg[1]['loc'][0]:
    #             msg = "password required"  
            
    #     else:
    #         if 'email' in msg[0]['loc'][0]:
    #             msg = "email required" 
    #         elif 'password' in msg[0]['loc'][0]: 
    #             msg = "password required"  
    except Exception as e:
        msg = str(e)
    return {
            'statusCode': 200,
            'headers': {
                # "Content-Type": "application/json",
                # "Access-Control-Allow-Origin": "*",
                # "Access-Control-Allow-Methods": "*",
                # 'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({"token":token,"msg":msg}, default=str)
            # 'body': {"msg":msg}
        } 
    # print(type(msg))    
    # print(msg)   


# def admin_login(event, context):
#     b = json.loads(event['body'])
#     token = []
#     msg = ""
#     try:
#         test = LoginTest(**b)
#         auth_data = { 'USERNAME':test.email , 'PASSWORD':test.password }        
#         resp = client.admin_initiate_auth(
#             UserPoolId=USER_POOL_ID, 
#             AuthFlow='ADMIN_USER_PASSWORD_AUTH', 
#             AuthParameters=auth_data, 
#             ClientId=USER_POOL_CLIENT_ID
#         )
#         token = resp       
#         msg = "Success!"       
#     except client.exceptions.NotAuthorizedException:
#         msg = "The username or password is incorrect"       
#     except client.exceptions.UserNotConfirmedException:
#         msg = "User is not confirmed"
#     except client.exceptions.UserNotFoundException:
#         msg = "User is not found"
#     except ValidationError as e:
#         msg = e.json()  
#         msg = msg.replace('\n', '')    # do your cleanup here
#         msg = json.loads(msg)
#         data_len = len(msg)
       
#         if data_len >1:
#             if 'email' in msg[0]['loc'][0]:
#                 msg = "email required"
#             elif 'password' in msg[1]['loc'][0]:
#                 msg = "password required"  
            
#         else:
#             if 'email' in msg[0]['loc'][0]:
#                 msg = "email required" 
#             elif 'password' in msg[0]['loc'][0]: 
#                 msg = "password required"  
#     except Exception as e:
#         msg = str(e)
#     return {
#             'statusCode': 200,
#             'headers': {
#                 "Content-Type": "application/json",
#                 "Access-Control-Allow-Origin": "*",
#                 "Access-Control-Allow-Methods": "*",
#                 "Access-Control-Allow-Headers": "*"
#             },
#             'body': json.dumps({"token:":token,"msg":msg}, default=str)
#             # 'body': {"msg":msg}
#         } 
#     # print(type(msg))    
#     # print(msg)   


# def admin_auth_challenge(event, context):
#     b = json.loads(event['body'])
#     token = []
#     msg = ""
#     try:
#         test = LoginTest(**b)
#         auth_data = { 'USERNAME':test.email , 'NEW_PASSWORD':test.password }        
#         resp = client.admin_respond_to_auth_challenge(
#             UserPoolId=USER_POOL_ID, 
#             ChallengeName='NEW_PASSWORD_REQUIRED', 
#             ChallengeResponses=auth_data, 
#             ClientId=USER_POOL_CLIENT_ID,
#             Session="AYABeCafcdMOnLHJA86gznetx3wAHQABAAdTZXJ2aWNlABBDb2duaXRvVXNlclBvb2xzAAEAB2F3cy1rbXMAS2Fybjphd3M6a21zOnVzLWVhc3QtMTo3NDU2MjM0Njc1NTU6a2V5L2IxNTVhZmNhLWJmMjktNGVlZC1hZmQ4LWE5ZTA5MzY1M2RiZQC4AQIBAHiAcAt7Ei832QLLvv5tnR-fAKEzaf-OMDg-j1aLh6qMVAGik7sqJqReSk0C_cdVY8bwAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMIRJU9eNoh1XzjT6XAgEQgDuc-livTQQIpQoEUnpIvlbSJ6-w1zGQMbyLzdek_5gQnX2QJK7Fm--cVojC5zpan3mw56L_Z2qI0GT4ggIAAAAADAAAEAAAAAAAAAAAAAAAAACL8o0OojPTqK_ljMEIQd0b_____wAAAAEAAAAAAAAAAAAAAAEAAADVr-KKqZdNkE2Nqo-AVNcXH8PmkYekr09TigKGUdwDITM00N46nQysygNoPY7ohWQw4djzNMpIGz8jfprf1erWbDMM7dut2RaMBPib06VXBnA6BsLsgP912tkrb7k5S1Mc9l3SrRbJ2qhxeOdZHkgMF1sD33SASY9rZ-YOUm9By69LpS8wIfkj33ZeVo9n_M1XBYr4iwGMNWiKeiD64rYHWtF7sY8ppsouz4vj-pSXR6BJCtQUIl2ZHO_3I2H-gT1bOyA8xaaNFCNpUEl7_9mnFSVc4kjgI9aOkbOkT61iH6DbHmxU9Q"
#         )
#         token = resp       
#         msg = "Success!"       
#     except client.exceptions.NotAuthorizedException:
#         msg = "The username or password is incorrect"       
#     except client.exceptions.UserNotConfirmedException:
#         msg = "User is not confirmed"
#     except client.exceptions.UserNotFoundException:
#         msg = "User is not found"
#     except ValidationError as e:
#         msg = e.json()  
#         msg = msg.replace('\n', '')    # do your cleanup here
#         msg = json.loads(msg)
#         data_len = len(msg)
       
#         if data_len >1:
#             if 'email' in msg[0]['loc'][0]:
#                 msg = "email required"
#             elif 'password' in msg[1]['loc'][0]:
#                 msg = "password required"  
            
#         else:
#             if 'email' in msg[0]['loc'][0]:
#                 msg = "email required" 
#             elif 'password' in msg[0]['loc'][0]: 
#                 msg = "password required"  
#     except Exception as e:
#         msg = str(e)
#     return {
#             'statusCode': 200,
#             'headers': {
#                 "Content-Type": "application/json",
#                 "Access-Control-Allow-Origin": "*",
#                 "Access-Control-Allow-Methods": "*",
#                 "Access-Control-Allow-Headers": "*"
#             },
#             'body': json.dumps({"token:":token,"msg":msg}, default=str)
#             # 'body': {"msg":msg}
#         } 
#     # print(type(msg))    
#     # print(msg)   
  

# def add_user_to_db(userId, email):
#     insert_data = {
#         'PK': 'USER#'+ userId,
#         'SK': 'USER#'+ userId,
#         'email': email,
#         'usr_id': userId,
#         'user_role': 'Author'
#     }
#     try:
#         table.put_item(Item=insert_data)
#         msg = 'insert success'
#     except ClientError as e:          
#         msg = e.response['Error']

#     return msg 


# def admin_registration(event, context):
#     b = json.loads(event['body'])  
#     signup_response = []
#     addgroup_response = []
#     msg = 'success!'
#     try:
#         signup_response = client.sign_up(
#                 ClientId=USER_POOL_CLIENT_ID,
#                 Username=b['email'],
#                 Password=b['password'],
#                 UserAttributes=[{'Name': 'email','Value': b['email']}])
#     except ClientError as e:
#         if e.response['Error']['Code'] == 'UsernameExistsException':
#             # Todo Handle Already Exists Email
#             msg="User already exists"
#         if e.response['Error']['Code'] == 'ParamValidationError':
#             # Todo Handle Param Validate
#             msg="Param Validate Error"
        

#     if msg == 'success!':
#         userId = signup_response['UserSub']        
#         try:
#             addgroup_response = client.admin_add_user_to_group(
#                 UserPoolId=USER_POOL_ID,
#                 Username=b['email'],
#                 GroupName='Admin'
#             ) 
#             insert = add_user_to_db(userId,b['email'])
#             if insert ==  'insert success':
#                 msg='success!'
#                 print("db success!")           
        
#         except ClientError as e:
#             if e.response['Error']['Code'] == 'NotAuthorizedException':
#                 # Todo Handle Already Exists Email
#                 msg="Unauthorized"
#             if e.response['Error']['Code'] == 'ParamValidationError':
#                 # Todo Handle Param Validate
#                 msg="Param Validate Error"
#             if e.response['Error']['Code'] == 'UserNotFoundException':
#                 # Todo Handle Already Exists Email
#                 msg="User not found"    

    
#     return {
#             'statusCode': 200,
#             'headers': {
#                 "Content-Type": "application/json",
#                 "Access-Control-Allow-Origin": "*",
#                 "Access-Control-Allow-Methods": "*",
#                 "Access-Control-Allow-Headers": "*"
#             },
#             'body': json.dumps({"msg":msg,"res":signup_response})
#             # 'body': {"msg":msg}
#         } 
         
   
# def user_profile_update(event, context):   
#     b = json.loads(event['body'])
#     usr_id = b['user_id']
#     usr_name = b['usr_name']
#     img_url = b['img_url']
#     key = {'PK': 'USER#'+usr_id,'SK': 'USER#'+usr_id}
#     response = table.update_item(
#         Key=key,
#         UpdateExpression="set usr_name= :a, img_url= :b", 
#         ExpressionAttributeValues={                
#                 ':a': usr_name,
#                 ':b': img_url
#             },
#         ReturnValues="UPDATED_NEW"
#         )
#     # return response['Items']
#     return {
#         "statusCode": 200,
#         'headers': {
#             'Access-Control-Allow-Headers': 'Content-Type',
#             'Access-Control-Allow-Origin': '*',
#             'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
#         },
#         "body": json.dumps(response)
#     }


# def get_user(event, context):
    # if event['httpMethod'] == "GET":
    #     response = client.admin_get_user(
    #         UserPoolId = USER_POOL_ID,
    #         Username = '06da8677-f786-4187-95a0-4424f350a24f'
    #     )

    #     # print(response['UserAttributes'])      
       
    #     return {
    #             'statusCode': 200,
    #             'headers': {
    #                 "Content-Type": "application/json",
    #                 "Access-Control-Allow-Origin": "*",
    #                 "Access-Control-Allow-Methods": "*",
    #                 "Access-Control-Allow-Headers": "*"
    #             },
    #             'body': json.dumps(response['UserAttributes'])
            # }