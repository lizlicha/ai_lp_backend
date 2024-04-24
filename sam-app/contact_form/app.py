import json
import boto3

def lambda_handler(event, context):
    # API Gateway からのリクエストボディを解析
    print(event['body'])
    body = json.loads(event['body'])
    print(type(body))

    # 環境変数からメール送信情報を取得
    SENDER = "noreply@encr.jp"  # 送信者メールアドレス
    RECIPIENT = "lizlicha1117@gmail.com"  # 受信者メールアドレス
    AWS_REGION = "ap-northeast-1"  # 適切なリージョンに変更してください
    SUBJECT = "コンタクトフォームからのメッセージ"
    CHARSET = "UTF-8"
    
    # メール本文を作成
    BODY_TEXT = f"Name: {body['name']}\nEmail: {body['email']}\nMessage: {body['message']}"

    # Amazon SES クライアントを作成
    client = boto3.client('ses',region_name=AWS_REGION)

    # メールを送信
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except Exception as e:
        print(e)
        raise e

    # レスポンスを返す
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'メッセージを送信しました。',
            'data': {'message':'message'} 
        }),
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,X-CSRF-TOKEN"}
    }
