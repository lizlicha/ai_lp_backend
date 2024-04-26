import os
import boto3

def lambda_handler(event, context):
    # インスタンスIDを環境変数から取得
    instance_id = os.environ['INSTANCE_ID']

    # EC2リソースを取得
    ec2 = boto3.resource('ec2')

    # インスタンスを停止
    instance = ec2.Instance(instance_id)
    response = instance.stop()

    return {
        'statusCode': 200,
        'body': f'Instance {instance_id} is stopping. Status: {response}'
    }
