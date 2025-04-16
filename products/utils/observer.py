
class Subject:
    def __init__(self):
        self.subscribers = []

    def attach(self, subscriber):
        self.subscribers.append(subscriber)

    def notify(self, data):
        for subscriber in self.subscribers:
            subscriber.update(data)


class LoggerObserver:
    def update(self, data):
        from .logger import Logger
        Logger().log(data)



class SystemNotificationObserver:
    def update(self, data):
        from products.models import Notification
        user = data.get("user")
        message = data.get("message")

        if user and message:
            Notification.objects.create(user=user, message=message)
