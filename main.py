import discord
from discord.ext import commands
import os
import json

def main():
    prefix='!'
    intents=discord.Intents.all() #봇이 멤버의 정보, 멤버 리스트를 불러옴
    
    client=commands.Bot(command_prefix=prefix, intents=intents) #commands_prefix는 접두사 의미 (!등록)

    scoreDict={}
    with open("data/score.json","w",encoding="utf-8") as f:
        json.dump(scoreDict,f,ensure_ascii=False)

    for filename in os.listdir('./cogs'):
        if '.py' in filename:
            filename = filename.replace('.py', '')
            client.load_extension(f"cogs.{filename}")
        
    with open('token.txt','r') as f:
        token=f.read() #토큰 읽어오기

    @client.event
    async def on_member_join(member):
        embed=discord.Embed(title='Hello!',description='%s님 안녕하세요\n흥챗봇 보려고 오셨나요? 환영합니다!\n가이드 명령어를 통해 기능을 확인해주세요!'%member.name,color=discord.Color.red())
        await member.guild.text_channels[0].send(embed=embed)

    @client.event
    async def on_member_remove(member):
        embed=discord.Embed(title='Bye!',description='%s님이 나가셨습니다'%member.name,color=discord.Color.red())
        await member.guild.text_channels[0].send(embed=embed)
        
    client.run(token) #생성한 Bot 객체에 토큰을 넣어 실행
    
if __name__ =='__main__':
    main()
