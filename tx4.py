import re
import logging
import os

# Создаем директорию для логов, если ее нет
notifications_path = os.path.join(os.getcwd(), 'notifications')
if not os.path.exists(notifications_path):
    os.mkdir(notifications_path)
os.chdir(notifications_path)

class Logerr:
    def __init__(self, log_file='log.txt'):
        self.log_file = log_file
        # Настройка логирования
        logging.basicConfig(filename=self.log_file, level=logging.INFO)

    def __call__(self, cls):
        """Декоратор, логирующий вызовы методов класса."""
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                # Оборачиваем методы класса в логирующий декоратор
                setattr(cls, attr_name, self.decorator(attr_name)(attr_value))
        return cls

    def decorator(self, method_name):
        def log_method(method):
            def wrapper(instance, *args, **kwargs):
                # Логируем вызов метода
                logging.info(f"Calling {instance.__class__.__name__}.{method_name}() with args={args}, kwargs={kwargs}")
                try:
                    result = method(instance, *args, **kwargs)
                    logging.info(f"{instance.__class__.__name__}.{method_name}() returned {result}")
                    return result
                except Exception as e:
                    logging.error(f"Error in {instance.__class__.__name__}.{method_name}(): {e}")
                    raise e
            return wrapper
        return log_method

    
@Logerr(log_file='log.txt')              
class Notification:
    def __init__(self, recipient, message):
        self.recipient = recipient
        self.message = message

    def send(self):
        print(f"notification to {self.recipient}: {self.message}")


class EmailValidate:
    def __set_name__(self, owner, name):
        self.name = "_" + name

    @staticmethod
    def is_valid_email(email):
        # Регулярное выражение для проверки адреса электронной почты
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def __set__(self, instance, value):
        if self.is_valid_email(value):
            instance.__dict__[self.name] = value
        else:
            raise ValueError("Invalid email address")

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]


@Logerr(log_file='log.txt')
class EmailNotification(Notification):
    recipient = EmailValidate()

    def __init__(self, recipient, message):
        super().__init__(recipient, message)


class SMSValidation:
    def __set_name__(self, owner, name):
        self.name = "_" + name

    @staticmethod
    def is_valid_phone(phone):
        # Регулярное выражение для проверки номера телефона
        pattern = r"^\+?\d{1,3}-?\d{1,14}$"
        return re.match(pattern, phone) is not None

    def __set__(self, instance, value):
        if self.is_valid_phone(value):
            instance.__dict__[self.name] = value
        else:
            raise ValueError("Invalid phone number")

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]


@Logerr(log_file='log.txt')
class SMSNotification(Notification):
    recipient = SMSValidation()

    def __init__(self, recipient, message):
        super().__init__(recipient, message)


class PushValidation:
    def __set_name__(self, owner, name):
        self.name = "_" + name

    @staticmethod
    def is_valid_token(token):
        if token is None:
            raise ValueError("Token is required")
        return True

    def __set__(self, instance, value):
        if self.is_valid_token(value):
            instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]


@Logerr(log_file='log.txt')
class PushNotification(Notification):
    recipient = PushValidation()

    def __init__(self, recipient, message):
        super().__init__(recipient, message)


# Пример использования

notification = EmailNotification("john@example.com", "Hello, world!")
notification.send()

sms_notification = SMSNotification("+79111234567", "Help, I'm in danger!")
sms_notification.send()

push_notification = PushNotification("my_push_token", "Don't forget to check your notifications!")
push_notification.send()
