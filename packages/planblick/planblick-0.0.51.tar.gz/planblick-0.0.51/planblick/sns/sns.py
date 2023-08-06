import boto3
import json
from cryptography.fernet import Fernet
import os
import base64

class Sns:
    def publish_event(self, correlationId, eventKind, payload):
        payload["correlationId"] = correlationId
        sns_client = boto3.client('sns', region_name='eu-central-1')
        key = json.loads(os.getenv("CLUSTER_CONFIG")).get("cipher-key")
        if key is None:
            raise Exception("Cipher key for encryption in sqs not set. I won't publish unencrypted")
        key = base64.urlsafe_b64encode(key.ljust(32)[:32].encode("utf-8"))
        cipher_suite = Fernet(key)
        sns_topic_arn = "arn:aws:sns:eu-central-1:282615081127:" + str(eventKind)
        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=cipher_suite.encrypt(json.dumps(payload).encode('utf-8')).decode('utf-8'),
            MessageStructure='raw')

        return response
