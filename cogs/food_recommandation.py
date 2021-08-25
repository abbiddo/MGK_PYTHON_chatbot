import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import asyncio
import json
from datetime import *
from random import *

class LunchRecommandation(commands.Cog):
    def __init__(self, client):
        self.client = client

        with open("./data/lunch.json","r",encoding="utf-8") as f:
            self.lunchDict=json.load(f)
#--------------------------------------------------------------        
    @commands.command(name = "메뉴추천")
    async def _lunchRecommandation(self,ctx):
        hour=datetime.now().hour
        if hour<5:
            day='야식'
        elif hour<12:
            day='아침'
        elif hour<18:
            day='점심'
        elif hour<24:
            day='저녁'
            
        def checkMessage(message):
            return message.author==ctx.author and message.channel==ctx.channel

        while True:
            re=0
            categories=list(self.lunchDict.keys())
            embed=discord.Embed(title='%s 맛집 추천'%day,description='%s중에 하나를 입력하세요'%categories,color=0xffa07a)
            await ctx.send(embed=embed)

            lunch=''
            try:
                while True:
                    message=await self.client.wait_for("message",timeout=60.0,check=checkMessage)

                    if message.content in categories:
                        lunch=choice(self.lunchDict[message.content])
                        embed=discord.Embed(title='%s 추천'%day,description="오늘 %s은 %s어떠세요? (좋아요/싫어요)"%(day,lunch),color=0xffa07a)
                        await ctx.send(embed=embed)
                        break
                    
                    embed=discord.Embed(title='오류 발생',description="정확한 답변을 입력하세요 : %s"%categories,color=discord.Color.red())
                    await ctx.send(embed=embed)

            except asyncio.TimeoutError:
                embed=discord.Embed(title='시간초과',description="명령어를 다시 입력하세요",color=discord.Color.red())
                await ctx.send(embed=embed)
                raise commands.CommandError('TimeOver')

            try:
                while True:
                    message=await self.client.wait_for("message",timeout=60.0,check=checkMessage)
                    if '좋아요' in message.content:
                        embed=discord.Embed(title='',description='지역을 입력 해주세요. %s 맛집을 찾아드릴게요!'%lunch,color=0xffa07a)
                        await ctx.send(embed=embed)

                        keyword=''
                        try:
                            area=await self.client.wait_for("message",timeout=60.0,check=checkMessage)
                            keyword=area.content+' '+lunch

                        except asyncio.TimeoutError:
                            embed=discord.Embed(title='시간초과',description="명령어를 다시 입력하세요",color=discord.Color.red())
                            await ctx.send(embed=embed)
                            raise commands.CommandError('TimeOver')

                        
                        url="https://www.mangoplate.com/search/%s"%keyword
            
                        headers={'User-Agent': 'Mozilla/5.0'}
                        response=requests.get(url, headers=headers)
                        soup=BeautifulSoup(response.text,"html.parser")
                        data=soup.select("li.server_render_search_result_item > div.list-restaurant-item")

                        if len(data)==0:
                            embed=discord.Embed(title='오류 발생',description='검색 결과가 없습니다',color=discord.Color.red())
                            await ctx.send(embed=embed)
                            raise commands.CommandError('No search results')
    
                        if len(data)>3:
                            limit=3
                        else:
                            limit=len(data)
            
                        embed=discord.Embed(title='맛집 추천',description='%s 맛집입니다'%keyword,color=0xffd770)
                        await ctx.send(embed=embed)
        
                        for i in data[:limit]:
                            image=i.select_one('img').get('data-original')
                            link=i.select_one('a').get('href')
                            title=i.select_one('h2.title').text.replace('\n', '')
                            rating=i.select_one('strong.search_point').text
                            category=i.select_one('p.etc').text
                            view=i.select_one('span.view_count').text
                            review=i.select_one('span.review_count').text

                            embed=discord.Embed(title=title,description=category,color=0xff8c0)
                            if len(rating)==0:
                                embed.add_field(name='평점',value='None')
                            else:
                                embed.add_field(name='평점',value=rating)

                            embed.add_field(name='조회수',value=view)
                            embed.add_field(name='리뷰 수',value=review,inline=True)
                            embed.add_field(name='링크',value='https://www.mangoplate.com%s'%link)

                            if 'https' in image:
                                embed.set_thumbnail(url=image)
                
                            await ctx.send(embed=embed)
                        break

                    elif '싫어요' in message.content:
                        embed=discord.Embed(title='',description='다른 음식을 추천 받으시겠어요?(네/아니오)',color=0xffa07a)
                        await ctx.send(embed=embed)

                        try:
                            while True:
                                message=await self.client.wait_for("message",timeout=60.0,check=checkMessage)
                                if message.content=='네':
                                    re=1
                                    break
                                elif message.content=='아니오':
                                    embed=discord.Embed(title='',description='맛집 추천을 종료합니다',color=discord.Color.red())
                                    await ctx.send(embed=embed)
                                    break
                                embed=discord.Embed(title='오류 발생',description="정확한 답변을 입력하세요 : 네/아니오",color=discord.Color.red())
                                await ctx.send(embed=embed)

                        except asyncio.TimeoutError:
                            embed=discord.Embed(title='시간초과',description="명령어를 다시 입력하세요",color=discord.Color.red())
                            await ctx.send(embed=embed)
                            raise commands.CommandError('TimeOver')
                            
                        break
                    
                    embed=discord.Embed(title='오류 발생',description="정확한 답변을 입력하세요 : 좋아요/싫어요",color=discord.Color.red())
                    await ctx.send(embed=embed)

            except asyncio.TimeoutError:
                embed=discord.Embed(title='시간초과',description="명령어를 다시 입력하세요",color=discord.Color.red())
                await ctx.send(embed=embed)
                raise commands.CommandError('TimeOver')

            if re!=1:
                break
#--------------------------------------------------------------
def setup(client):
    client.add_cog(LunchRecommandation(client))
