from functools import wraps
from chatbottokenizer import Tokenizer


def message(router: 'Router', template: str):
    def decorator(func):
        router.add(template, func)

        @wraps(func)
        async def wrapper(*args, **kwargs):
            await func(*args, **kwargs)

        return wrapper

    return decorator


def guide(router: 'Router'):
    def decorator(func):
        router.set_guide(func)

        @wraps(func)
        async def wrapper(*args, **kwargs):
            await func(*args, **kwargs)

        return wrapper

    return decorator


class Router:
    commands = []
    guide = None

    def __init__(self, name: str):
        self.name = name

    def add(self, template, func):
        self.commands.append((template, func))

    def set_guide(self, func):
        self.guide = func

    async def __call__(self, message: 'discord.Message'):
        tokens = Tokenizer(self.name, message.content)

        if not tokens.to_bot():
            return

        for (tmpl, func) in self.commands:
            if tokens.match(tmpl):
                await func(
                    self,
                    items=tokens.items(),
                    message=message,
                    send=message.channel.send)
                return
        if self.guide != None:
            await func(self, message=message, send=message.channel.send)
