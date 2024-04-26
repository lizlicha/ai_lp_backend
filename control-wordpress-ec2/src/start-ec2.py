import boto3

def lambda_handler(event, context):
    # インスタンスIDを環境変数から取得
    instance_id = os.environ['INSTANCE_ID']

    # EC2リソースを取得
    ec2 = boto3.resource('ec2')

    # インスタンスを起動
    instance = ec2.Instance(instance_id)
    response = instance.start()

    return {
        'statusCode': 200,
        'body': f'Instance {instance_id} is starting. Status: {response}'
    }
