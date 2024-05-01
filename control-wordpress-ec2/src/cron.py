import boto3
import json

def lambda_handler(event, context):

    # 
    if "challenge" in event["body"]:
        body=json.loads(event["body"])
        return {
            'statusCode': 200,
            'body': body["challenge"]
        }
        
    # 起動
    if "起動" in event["body"]:
        functionName='wordpress_start_ec2'

    # 停止
    if "停止" in event["body"]:
        functionName='wordpress_stop_ec2'

    # lambda呼び出し
    response = boto3.client('lambda').invoke(
        FunctionName = functionName,
        InvocationType='RequestResponse'
        )
    print(response)

    return {
        'statusCode': 200,
        'body': f'ok'
    }
