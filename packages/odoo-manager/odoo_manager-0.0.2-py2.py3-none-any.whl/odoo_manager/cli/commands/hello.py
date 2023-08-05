from .base import BaseCommand


class Hello(BaseCommand):
    def run(self):
        print('Hello!')
