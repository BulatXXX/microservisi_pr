import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='tasks')

message = {
    "title": "RABBIT MQ",
    "description": "Do something important",
    "datetime": "2024-12-26T14:00:00",
    "assigned_to": None
}

channel.basic_publish(exchange='', routing_key='tasks', body=json.dumps(message))
print("Message sent!")
connection.close()