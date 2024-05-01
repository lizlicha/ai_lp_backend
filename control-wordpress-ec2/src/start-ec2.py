import boto3
import os
import json
import requests
import datetime

def write_to_dynamodb(instance_id, status):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('EC2InstanceState')
    response = table.put_item(
       Item={
            'InstanceId': instance_id,
            'Status' : status
        }
    )
    return response

def start_ec2():
    # インスタンスIDを環境変数から取得
    instance_id = os.environ['INSTANCE_ID']
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']

    # EC2リソースを取得
    ec2 = boto3.resource('ec2')

    # インスタンスを起動
    instance = ec2.Instance(instance_id)
    #response = instance.start()
    write_to_dynamodb(instance_id,'1')

def send_message_to_sqs(channel, message):
    # SQSクライアントの初期化
    sqs = boto3.client('sqs')
    
    # SQSキューにメッセージを送信
    body = {'Channel':channel,'Message':message}
    response = sqs.send_message(
        QueueUrl='https://sqs.ap-northeast-1.amazonaws.com/908725951096/send_slack',
        MessageBody=json.dumps(body,ensure_ascii=False)
    )
    return response

def lambda_handler(event, context):

    start_ec2()        

    # slackに通知
    send_message_to_sqs('01_wordpress','起動したよ')

    return {
        'statusCode': 200
    }
