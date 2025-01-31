from django.core.management.base import BaseCommand
import json
import os
# from PIL import Image
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from tv_programs.models import TVChannel, TVProgram
from .get_tv_schedule import Command as GetCommand
from base64 import b64decode
from django.core.files.base import ContentFile
from django.db.models import DateTimeField
from django.db.models.functions import Cast
import datetime
from django.utils import timezone
import pytz


class Command(BaseCommand):
    help = 'Import films from json file'

    def is_file_exists(self, file_obj):
        return bool(file_obj.name) and file_obj.storage.exists(file_obj.name)

    def handle(self, *args, **options):
        self.create_channels()
        self.create_schedule()


    def create_channel(self, channel_json):
            attrs = {"name": channel_json["name"]}
            channel_obj, created = TVChannel.objects.update_or_create(name=channel_json["name"],
                                                 defaults=attrs)

            if self.is_file_exists(channel_obj.logo):
                return     
            image_data = b64decode(channel_json["logo_b64"])
            image_logo = ContentFile(image_data, f"{channel_json["name"]}.jpg")
            channel_obj.logo = image_logo
            channel_obj.save()

    def create_program(self, program_json):
        print(program_json["channel_name"])
        tv_channel = TVChannel.objects.get(name=program_json["channel_name"])
        date = datetime.datetime.strptime(program_json["date"], "%Y-%m-%dT%H:%M:%S") 
        attrs = {"title": program_json["title"], "date": date, "tv_channel": tv_channel}
        program_obj = TVProgram.objects.update_or_create(date=program_json["date"],
                                           defaults=attrs)[0]
        program_obj.save()

    def create_channels(self):
        with open(GetCommand.filename("channel"), 'r') as f:
            channels_data = json.load(f)
            for channel_date in channels_data["channels"]:
                self.create_channel(channel_date)

    def create_schedule(self):
        with open(GetCommand.filename("schedule"), 'r') as f:
            schedule_data = json.load(f)
            for program in schedule_data["schedule"]:
                self.create_program(program)