import os
import boto3
import json
import requests
import datetime

def lambda_handler(event, context):
    # インスタンスIDを環境変数から取得
    instance_id = os.environ['INSTANCE_ID']

    # EC2リソースを取得
    ec2 = boto3.resource('ec2')

    # インスタンスを停止
    instance = ec2.Instance(instance_id)
    response = instance.stop()

    # slackに通知
    SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/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'
    try:
        payload = {
            'attachments': [
                {
                    'color': '#36a64f',
                    'pretext': '停止したよ',
                    'text': str(datetime.datetime.now())
                }
            ]
        }
        response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
    except requests.exceptions.RequestException as e:
        print(e)
    else:
        print(response.status_code)
        
    return {
        'statusCode': 200,
        'body': f'Instance {instance_id} is stopping. Status: {response}'
    }
