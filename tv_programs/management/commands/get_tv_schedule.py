from django.core.management.base import BaseCommand
import requests
import bs4 as bs
from dataclasses import dataclass, asdict
import datetime
import re
import json


@dataclass
class TVChannel: # Телеканал
    name: str # Название
    logo_b64: str # Логотип в base64


@dataclass
class TVProgram: # Телепрограмма
    channel_name: str # Название телеканала
    title: str # Название
    date: datetime.datetime # Дата начала


@dataclass
class TVSchedule: # Расписание телепрограмм
    schedule: list[TVProgram]


@dataclass
class TVChannels:
    channels: list[TVChannel]


class TextCleaner:
    @staticmethod
    def clean_text(text):
        return re.sub(r"\t", "", text)


class Command(BaseCommand):
    help = 'Download json via https://www.tricolor.ru/local/api/program/getProgram/'

    def handle(self, *args, **options):
        tv_channels, tv_schedule = self.get_tv_programs()
        with open(self.filename("channel"), "w", encoding="utf-8") as f:
            json.dump(asdict(tv_channels), f, ensure_ascii=False, indent=4)
        with open(self.filename("schedule"), "w", encoding="utf-8") as f:
            json.dump(asdict(tv_schedule), f, ensure_ascii=False, indent=4)

    @staticmethod
    def filename(category):
        PATH = "tv_programs/data/"
        match category:
            case "channel":
                return PATH + "channels.json"
            case "schedule":
                return PATH + "schedule.json"

    
    @staticmethod
    def get_tv_programs():
        def __parse_date_title(div_element, sched_date, channel_name):
            try:
                print(div_element.find("span").text)
                hour_minute = datetime.datetime.strptime(div_element.find("span").text, "%H:%M")
                prog_date = sched_date.replace(hour=hour_minute.hour, minute=hour_minute.minute).isoformat()
                title = TextCleaner.clean_text(div_element.find("p").text)
                return TVProgram(title=title, channel_name=channel_name, date=prog_date)
            except (TypeError, ValueError):
                return None
            
        tv_schedule: TVSchedule = TVSchedule(list())
        tv_channels: TVChannels = TVChannels(list())

        for page_num in range(4):
            resp = requests.get(f"https://glaz-ok.online/get-content?page={page_num}&program=true", params={
                "pageNum": 0,
            })
            soup = bs.BeautifulSoup(resp.text, "html.parser")
            
            tv_programs = soup.findAll("li")
            for program in tv_programs:
                a_containers = program.findAll("a")

                name = a_containers[0].find("p").text
                img_b64 = re.findall(",.*", a_containers[0].find("img").get("src"))[0][1:]
                tv_channel = TVChannel(name=name, logo_b64=img_b64)
                tv_channels.channels.append(tv_channel)
                print(f"Proccesing channel: {name}")

                schedule_link = a_containers[1].get("href")
                resp = requests.get(schedule_link)
                soup = bs.BeautifulSoup(resp.text, "html.parser")
                whole_schedule = soup.find("ul", class_="tab-content").findAll("li")
                for day in whole_schedule:
                    date = datetime.datetime.strptime(day.get("id"), "%d-%m-%Y")
                    day_schedule = [i for i in day.findAll("div") if i.contents] # Removes div elements with no children
                    prikols = list(map(__parse_date_title, day_schedule, [date] * len(day_schedule), [tv_channel.name] * len(day_schedule)))
                    tv_schedule.schedule.extend(prikols)
        
        # Clear none
        tv_schedule.schedule = [i for i in tv_schedule.schedule if i is not None]
        
        return (tv_channels, tv_schedule)