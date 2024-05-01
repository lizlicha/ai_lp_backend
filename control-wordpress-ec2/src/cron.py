import boto3
import json
import os
import requests

dynamodb = boto3.resource('dynamodb')
slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
instance_id = os.environ['INSTANCE_ID']

def read_from_dynamodb(instance_id):
    table = dynamodb.Table('EC2InstanceState')
    response = table.get_item(
        Key={
            'InstanceId': instance_id
        }
    )
    item = response.get('Item', {})
    print(item)
    return item

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

    # DynamoDBからデータを読み込む
    item = read_from_dynamodb(instance_id)
    
    # 空の時はレコード作成
    if not item:
        write_to_dynamodb(instance_id,0)
        return

    status = item['Status']
    if status == '0':
        #0の時はおわり
        return
    elif status == '1':
        #1の時はメッセージ投げてインクリメント
        send_message_to_sqs('01_wordpress','30分後に停止するよ')
        write_to_dynamodb(instance_id,'2')

    elif status == '2':
        #2の時は終了
        # lambda呼び出し
        response = boto3.client('lambda').invoke(
            FunctionName = 'wordpress_end_ec2',
            InvocationType='RequestResponse'
            )
        write_to_dynamodb(instance_id,'0')
        print(response)
    
    return {
        'statusCode': 200,
        'body': f'ok'
    }
