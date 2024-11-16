import pika
import json
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task import Task, TaskStatus  # Убедитесь, что импорт соответствует вашей структуре проекта

# Настройки RabbitMQ
RABBITMQ_HOST = "rabbitmq"  # Имя RabbitMQ-контейнера в docker-compose
RABBITMQ_QUEUE = "tasks_queue"  # Название вашей очереди

def process_message(channel, method, properties, body):
    """Обрабатывает сообщение из RabbitMQ."""
    try:
        message = json.loads(body)
        title = message["title"]
        description = message["description"]
        datetime = message["datetime"]
        status = message.get("status", "CREATED")

        # Валидация даты
        from datetime import datetime as dt
        if not dt.strptime(datetime, "%Y-%m-%dT%H:%M:%S"):
            raise ValueError("Invalid datetime format")

        # Запись в базу данных
        db: Session = next(get_db())
        new_task = Task(title=title, description=description, datetime=datetime, status=status)
        db.add(new_task)
        db.commit()

        print(f"Task '{title}' added successfully!")
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Failed to process message: {e}")
        channel.basic_nack(delivery_tag=method.delivery_tag)

def consume_messages():
    """Настраивает подключение к RabbitMQ и прослушивание очереди."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=process_message)
    print("Waiting for messages...")
    channel.start_consuming()