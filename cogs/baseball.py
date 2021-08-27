import asyncio
import discord
from discord.ext import commands
from random import *

class Baseball(commands.Cog):
    def __init__(self, client):
        self.client=client
#--------------------------------------------------------------        
    @commands.command(name = "숫자야구")
    async def _baseball(self,ctx):
        embed=discord.Embed(title='숫자 야구 게임',description='숫자를 맞추는 게임입니다\n숫자와 자리가 일치한다면 Strike\n숫자는 일치하지만 자리가 일치하지 않으면 Ball\n\n난이도를 선택해주세요 (상 중 하)',color=discord.Color.blue()) 
        await ctx.send(embed=embed)

        def checkAnswer(message):
            return message.channel==ctx.channel

        message=await self.client.wait_for("message",check=checkAnswer)

        num=[]
        if message.content=='하':
            n=3

        elif message.content=='중':
            n=4

        else:
            n=5
            
        while len(num)<n:
            a=randint(0,9)
            if a not in num:
                num.append(a)

        embed=discord.Embed(title=message.content,description='%s 자리 숫자를 입력해주세요 (ex : 209)'%n,color=discord.Color.blue())
        await ctx.send(embed=embed)
        
        cnt=0
        while True:
            strike=0
            ball=0

            message=await self.client.wait_for("message",check=checkAnswer)

            lst=[]
            for i in message.content:
                lst.append(int(i))

            for i in range(len(lst)):
                for j in range(len(num)):
                    if lst[i]==num[j]:
                        if i==j:
                            strike+=1
                        else:
                            ball+=1
                    
            cnt+=1

            embed=discord.Embed(title='',description='%s Strike, %s Ball'%(strike,ball),color=0xffa07a)
            await ctx.send(embed=embed)
                
            if strike==len(num):
                embed=discord.Embed(title='Win',description='%s님 정답입니다\n%s번째 승리하였습니다'%(message.author.name,cnt),color=discord.Color.red())
                await ctx.send(embed=embed)
                break
#--------------------------------------------------------------   
def setup(client):
    client.add_cog(Baseball(client))
