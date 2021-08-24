import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import asyncio

class Food(commands.Cog):
    def __init__(self, client):
        self.client = client
#--------------------------------------------------------------        
    @commands.command(name='맛집')
    async def _맛집(self,ctx,*food):
        if food==():
            embed=discord.Embed(title='오류 발생',description='검색어를 입력해주세요',color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            food='%s'%(' '.join(food))

        url="https://www.mangoplate.com/search/%s"%food
            
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
            
        embed=discord.Embed(title='맛집 추천',description='%s 맛집입니다'%food,color=0xffd770)
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
#--------------------------------------------------------------
def setup(client):
    client.add_cog(Food(client))
