import boto3
import json

class Sns:
    def publish_event(self, correlationId, eventKind, payload):
        payload["correlationId"] = correlationId
        sns_client = boto3.client('sns', region_name='eu-central-1')

        sns_topic_arn = "arn:aws:sns:eu-central-1:282615081127:" + str(eventKind)
        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=json.dumps(payload),
            MessageStructure='raw')

        return response
