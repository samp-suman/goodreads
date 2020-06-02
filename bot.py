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
        # For hello-Greetings
        if message.content.startswith('~gdhello'):
            await message.channel.send('Hello {0.author.mention}.\n Use **~help** for use commands.'.format(message))

        # For Help
        if message.content == "~gdhelp":
            embed = discord.Embed(title="Help on BOT", description="Some useful commands")
            embed.add_field(name="~gdhello", value="Greets the user")
            embed.add_field(name="**~gdbook** <**book-title/ISBN**>", value="eg:- ~gdbook ikagai")
            embed.add_field(name="~gdauthor <**author name**>", value="~gdauthor mark manson")
            await message.channel.send(content=None, embed=embed)

        # For Book Search
        if message.content.startswith('~gdbook'):
            print(str(message.content).split(' '))
            title = '+'.join(str(message.content).split(' ')[1:])
            if title:
                raw, des = searchTitle(title)
                if raw:
                    title = raw.title.text
                    author = raw.author.find('name').text
                    img_url = raw.image_url.text
                    book_url = 'https://www.goodreads.com/book/show/{}'.format(raw.best_book.id.text)
                    embed = discord.Embed(title=title, description="**Author: {}**\n{}".format(author, des), colour=discord.Colour.teal(), url=book_url, img_url=img_url)
                    embed.set_image(url=img_url)
                    await message.channel.send(embed=embed, content=None)
                else:
                    await message.channel.send("Not Found Try somethimg else {0.author.mention}".format(message))
            else:
                await message.channel.send("Enter title after !search eg. !search ikagai {0.author.mention}".format(message))

        # For User Search
        if message.content.startswith('~gduser'):
            print(str(message.content).split(' '))
            user_name = '+'.join(str(message.content).split(' ')[1:])
            if user_name:
                name, user_link, last_active, img_url = getUserDetails(user_name)

                if user_link:
                    embed = discord.Embed(title=name, description="User-Name: **{}**\nLast Active:- **{}**".format(user_name, last_active),
                                          colour=discord.Colour.dark_blue(), url=user_link)
                    embed.set_image(url=img_url)
                    await message.channel.send(embed=embed, content=None)
                else:
                    await message.channel.send("Not Found Try somethimg else {0.author.mention}".format(message))
            else:
                await message.channel.send(
                    "Enter title after !search eg. !search Paulo Coelho {0.author.mention}".format(message))

        # For Author Search
        if message.content.startswith('~gdauthor'):
            print(str(message.content).split(' '))
            author = '+'.join(str(message.content).split(' ')[1:])
            if author:
                author_id = getAuthorId(author)
                title, des, url, img_url = getAuthorDetails(author_id)
                if author_id:
                    embed = discord.Embed(title=title, description=des,
                                          colour=discord.Colour.dark_green(), url=url)
                    embed.set_image(url=img_url)
                    await message.channel.send(embed=embed, content=None)
                else:
                    await message.channel.send(
                        "Not Found Try somethimg else {0.author.mention}".format(message))
            else:
                await message.channel.send(
                    "Enter title after !search eg. !search Paulo Coelho {0.author.mention}".format(message))


client = MyClient()

def searchTitle(title):
    url = URL + '?q=' + title + '&page=1&' + 'key=' + API_KEY
    print(url)
    response = requests.get(url)
    if response:
        raw = BeautifulSoup(response.text, 'html.parser')
        des = getDescription(raw.best_book.id.text)
        return raw, des
    else:
        return None


def getAuthorId(author):
    url = URL + '?q=' + author + '&page=1&' + 'key=' + API_KEY
    print(url)
    response = requests.get(url)
    if response:
        raw = BeautifulSoup(response.text, 'html.parser')
        author_id = raw.author.find('id').text
        return author_id
    else:
        return None


def getDescription(id):
    u = "https://www.goodreads.com/book/show/{}".format(id)
    print(u)
    res = requests.get(u)
    if res:
        raw_des = BeautifulSoup(res.content, 'html.parser')
        des = raw_des.find('div', attrs={'id': 'description'}).span.text

        return des
    else:
        return None


def getAuthorDetails(author_id):
    url = "https://www.goodreads.com/author/show/{}".format(author_id)
    print(url)
    res = requests.get(url)
    if res:
        raw = BeautifulSoup(res.content, 'html.parser')
        title = raw.title.text
        if raw.find('div', attrs={'class': 'aboutAuthorInfo'}).span:
            des = raw.find('div', attrs={'class': 'aboutAuthorInfo'}).span.text
        else:
            des = None
        if raw.find('div', attrs={'class': 'leftContainer authorLeftContainer'}).img:
            img_url = raw.find('div', attrs={'class': 'leftContainer authorLeftContainer'}).img['src']
        else:
            img_url = None
        return title, des, url, img_url
    else:
        return None


def getUserDetails(username):
    url = "https://www.goodreads.com/user/show.xml?id=false&key=PV3GOHI0lJBNHlsS2CFxlw&username={}".format(username)
    res = requests.get(url)
    if res:
        raw = BeautifulSoup(res.content,'xml')
        name = raw.user.find('name').text
        user_link = raw.user.link.text
        last_active = raw.user.last_active.text
        img_url = raw.user.image_url.text
        return name, user_link, last_active, img_url

    else:
        return None

client.run(TOKEN)