import discord
from discord.ext import commands
import json
from random import *

class Lunch(commands.Cog):
    def __init__(self, client):
        self.client = client

        with open("./data/lunch.json","r",encoding="utf-8") as f:
            self.lunchDict=json.load(f)

#--------------------------------------------------------------        
    @commands.command(name = "점심추천")
    async def recommand_lunch(self,ctx,kind1=None,kind2=None):
        if kind1==None:        
            categories=list(self.lunchDict.keys()) # ['한식','중식'....]
            category=choice(categories) # ex) 한식
            lunch=choice(self.lunchDict[category]) #ex) 삼겹살
            embed=discord.Embed(title='점심',description="오늘 점심은 %s, 그 중에서 %s 어떠세요?"%(category,lunch),color=0xffa07a)
            await ctx.send(embed=embed)

        elif kind2 == None:
            lunch=choice(self.lunchDict[kind1])
            embed=discord.Embed(title='점심',description="오늘 점심은 %s 어떠세요?"%(lunch),color=0xffa07a)
            await ctx.send(embed=embed)

        elif kind1!=None and kind2!=None:
            categories=[]
            categories.append(kind1)
            categories.append(kind2)            
            category=choice(categories)
            lunch=choice(self.lunchDict[category])
            embed=discord.Embed(title='점심',description="%s이랑 %s이면... 오늘 점심은 %s 어떠세요?"%(kind1,kind2,lunch),color=0xffa07a)
            await ctx.send(embed=embed)
#--------------------------------------------------------------
            
def setup(client):
    client.add_cog(Lunch(client))
