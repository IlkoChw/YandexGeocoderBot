from time import sleep
from django.core.management.base import BaseCommand
from app_main.bot_logic import *
from app_main.utils import create_groups_and_permissions


class Command(BaseCommand):

    def handle(self, *args, **options):
        create_groups_and_permissions()
        while True:
            try:
                bot.polling(none_stop=True, interval=0)
            except Exception as e:
                print(e)
                sleep(5)
