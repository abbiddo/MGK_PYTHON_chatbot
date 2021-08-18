from discord.ext import commands
import discord
from datetime import *

class Today(commands.Cog):
    def __init__(self, client):
        self.client = client
        
#--------------------------------------------------------------        
    @commands.command(name='날짜')
    async def _날짜(self,ctx):
        now=datetime.now()
        embed=discord.Embed(title='',description="오늘은 %d년 %d월 %d일 입니다."%(now.year,now.month,now.day),color=0x7fffd4)
        await ctx.send(embed=embed)
#--------------------------------------------------------------
    @commands.command(name='시간')
    async def _시간(self,ctx):
        now=datetime.now()
        embed=discord.Embed(title='',description="현재시각은 %d시 %d분 %d초 입니다."%(now.hour,now.minute,now.second),color=0x7fffd4)
        await ctx.send(embed=embed)
#--------------------------------------------------------------   
    
def setup(client):
    client.add_cog(Today(client))
