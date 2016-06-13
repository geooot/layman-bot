import discord
import layman
import asyncio

client = discord.Client()
allowed_servers = []

@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name, client.user.id)
    print('------')

@client.event
@asyncio.coroutine
def on_message(message):
    if not message.author.bot:
        if message.content.startswith('!startreading'):
            allowed_servers.append(message.channel)
            yield from client.send_message(message.channel, '--layman-script started in #' + message.channel.name + ' on ' + message.server.name + '--')
            print(allowed_servers)
        elif message.content.startswith('!stopreading'):
            allowed_servers.remove(message.channel)
            print(allowed_servers)
            yield from client.send_message(message.channel, '--layman-script stopped in #' + message.channel.name + ' on ' + message.server.name + '--')
        elif message.content.startswith('!memory'):
            yield from client.send_message(message.channel, "```" + layman.get_memory_as_str() + " ```")
        elif message.content.startswith('!laymanhelp'):
            x = 1
            yield from client.send_message(message.channel, '`!laymanhelp` This message \n \n`!startreading` Start parsing sent messages\n \n`!stopreading` Start parsing sent messages\n \n`!memory` Show memory from messages \n \n')
            yield from client.send_message(message.channel, '**Check out more information about layman-script @ http://geooot.com/layman-script**')
        elif message.content.startswith('!q'):
            msg = message.content
            a = layman.interpret(msg)
            yield from client.send_message(message.channel, "` " + str(a) + " `")
        else:
            msg = message.content.lower().replace("?","").replace(" i ", " " + message.author.name + " ").replace("i ", message.author.name + " ").replace(" i", message.author.name + " ")
            # print(msg)
            if message.channel in allowed_servers:
                print("[" + str(message.author) + " @ #" + message.channel.name + " on " + message.server.name  + "] " +  message.content)
                a = layman.interpret(msg)
                if a != "":
                    yield from client.send_message(message.channel, "` " + str(a) + " `")

@client.event
@asyncio.coroutine
def on_server_join(server):
    yield from client.send_message(server.channels[0], 'Hola ' + server.name + "! I read your messages and can answer questions based on the messages. Check out my commands at `!laymanhelp`. ")

client.run('your_token_here')
