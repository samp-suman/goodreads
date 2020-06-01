# Work with Python 3.6
import discord
import requests
from bs4 import BeautifulSoup



API_KEY = "PV3GOHI0lJBNHlsS2CFxlw"
URL = "https://www.goodreads.com/search/index.xml"


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


TOKEN = read_token()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!hello'):
            await message.channel.send('Hello {0.author.mention}'.format(message))

        if message.content.startswith('!search'):
            print(str(message.content).split(' '))
            title = '+'.join(str(message.content).split(' ')[1:])
            if title:
                raw = searchTitle(title)
                if raw:
                    title = raw.title.text
                    author = raw.author.find('name').text
                    #img_url = raw.image_url.text
                    book_url = 'https://www.goodreads.com/book/show/{}'.format(raw.best_book.id.text)
                    await message.channel.send("Title:  {0}\n Author:  {1}\n{2}{3.author.mention}".format(title, author,book_url, message))
                else:
                    await message.channel.send("Not Found Try somethimg else {0.author.mention}".format(message))
            else:
                await message.channel.send("Enter title after !search eg. !search ikagai {0.author.mention}".format(message))

client = MyClient()

def searchTitle(title):
    url = URL + '?q=' + title + '&page=1&' + 'key=' + API_KEY
    print(url)
    response = requests.get(url)
    if response:
        raw = BeautifulSoup(response.text, 'xml')
        return raw
    else:
        return None
client.run(TOKEN)