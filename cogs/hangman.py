import asyncio
import discord
from discord.ext import commands
from random import *
import requests
from bs4 import BeautifulSoup

class Hangman(commands.Cog):
    def __init__(self, client):
        self.client=client
#--------------------------------------------------------------        
    @commands.command(name = "행맨")
    async def _hangman(self,ctx):
        embed=discord.Embed(title='행맨',description='행맨 게임입니다',color=discord.Color.blue())
        await ctx.send(embed=embed)

        def checkAnswer(message):
            return message.author==ctx.author and message.channel==ctx.channel
        
        word_url='https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=오늘의 단어'
        raw=requests.get(word_url)
        soup=BeautifulSoup(raw.text, 'html.parser')
        box=soup.find_all('a', {'class' : 'word'})
        box2=soup.find_all('span',{'class':'mean'})

        words=[]

        for page in box:
            words.append(page.find('strong').text)
            
        answer=choice(words)
        idx=words.index(answer)
        
        letters=''
        be=0

        for i in range(len(answer)):
            if answer[i] == ' ':
                letters+='  '
            else:
                letters+='- '
                be+=1

        be*=2

        while be!=0:
            embed=discord.Embed(title='',description='%s\n기회 %s번 남았습니다'%(letters,be),color=0xffa07a)
            await ctx.send(embed=embed)
            
            message=await self.client.wait_for("message",check=checkAnswer)
            spell=message.content

            if spell in answer:
                for i in range(len(answer)):
                    if spell==answer[i]:
                        letters=letters[:2*i]+spell+' '+letters[2*i+2:]

            if '-' not in letters:
                embed=discord.Embed(title="승",description='답은 **%s**(%s)입니다'%(answer,box2[idx].text),color=discord.Color.blue())
                await ctx.send(embed=embed)
                break
            
            be-=1

        if be==0:
            embed=discord.Embed(title="패",description='답은 **%s**(%s)입니다'%(answer,box2[idx].text),color=discord.Color.red())
            await ctx.send(embed=embed)
#--------------------------------------------------------------   
def setup(client):
    client.add_cog(Hangman(client))
