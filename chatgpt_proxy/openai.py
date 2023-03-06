import openai
import os


class SingletonCls(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonCls, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class OpenAiCli(object):
    __metaclass__ = SingletonCls

    def __init__(self):
        openai.organization = os.environ['OPENAI_ORG']
        openai.api_key = os.environ['OPENAI_KEY']
        self.model = 'gpt-3.5-turbo'

    def chat(self, messages: list):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages
        )
        replyContent = response['choices'][0]['message']['content']
        return replyContent
