import discord
from discord.ext import commands
import json
from random import *
from datetime import *

class Food(commands.Cog):
    def __init__(self, client):
        self.client = client

        with open("./data/lunch.json","r",encoding="utf-8") as f:
            self.lunchDict=json.load(f)

#--------------------------------------------------------------        
    @commands.command(name = "메뉴")
    async def recommand_food(self,ctx,kind1=None,kind2=None):
        hour=datetime.now().hour
        if hour<5:
            day='야식'
        elif hour<12:
            day='아침'
        elif hour<18:
            day='점심'
        elif hour<24:
            day='저녁'
            
        if kind1==None:        
            categories=list(self.lunchDict.keys()) # ['한식','중식'....]
            category=choice(categories) # ex) 한식
            lunch=choice(self.lunchDict[category]) #ex) 삼겹살
            embed=discord.Embed(title='%s'%day,description="오늘 %s은 %s, 그 중에서 %s 어떠세요?"%(day,category,lunch),color=0xffa07a)
            await ctx.send(embed=embed)

        elif kind2 == None:
            lunch=choice(self.lunchDict[kind1])
            embed=discord.Embed(title='%s'%day,description="오늘 %s은 %s 어떠세요?"%(day,lunch),color=0xffa07a)
            await ctx.send(embed=embed)

        elif kind1!=None and kind2!=None:
            categories=[]
            categories.append(kind1)
            categories.append(kind2)            
            category=choice(categories)
            lunch=choice(self.lunchDict[category])
            embed=discord.Embed(title='%s'%day,description="%s이랑 %s이면... 오늘 %s은 %s 어떠세요?"%(kind1,kind2,day,lunch),color=0xffa07a)
            await ctx.send(embed=embed)
#--------------------------------------------------------------
            
def setup(client):
    client.add_cog(Food(client))
