import boto3
import json

def lambda_handler(event, context):

    # チャレンジ認証    
    if "challenge" in event["body"]:
        body=json.loads(event["body"])
        return {
            'statusCode': 200,
            'body': body["challenge"]
        }

    body = json.loads(event["body"])
    text = body["event"]["text"]
    print(text)
    
    functionName = None
        
    # 起動
    if "起動" in text:
        functionName='wordpress_start_ec2'

    # 停止
    if "停止" in text:
        functionName='wordpress_end_ec2'

    # lambda呼び出し
    if functionName:
        response = boto3.client('lambda').invoke(
            FunctionName = functionName,
            InvocationType='Event'
            )
        print(response)

    return {
        'statusCode': 200,
        'body': f'ok'
    }
