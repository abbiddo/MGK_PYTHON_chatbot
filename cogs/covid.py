import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

class Covid(commands.Cog):
    def __init__(self, client):
        self.client = client
#--------------------------------------------------------------        
    @commands.command(name='코로나')
    async def _코로나(self,ctx):
        url='https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98+%ED%99%95%EC%A7%84%EC%9E%90'
        raw=requests.get(url)
        soup=BeautifulSoup(raw.text,"html.parser")
        box=soup.find('li', {'class':'info_01'})
        total=box.find_all('p')
        yesterday=box.find_all('em')
        embed=discord.Embed(title='코로나 확진자 수',description="전 날 확진자 수는 %s명이고, 누적 확진자 수는 %s명 입니다."%(yesterday[0].text,total[0].text),color=0xff4500)
        await ctx.send(embed=embed)
#--------------------------------------------------------------
def setup(client):
    client.add_cog(Covid(client))
