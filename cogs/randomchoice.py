import discord
from discord.ext import commands
from random import *

class Random(commands.Cog):
    def __init__(self, client):
        self.client=client
#--------------------------------------------------------------        
    @commands.command(name = "숫자뽑기")
    async def _randomchoice(self,ctx):
        embed=discord.Embed(title='랜덤 숫자 뽑기',description='랜덤으로 숫자를 뽑습니다\n(최소값 최대값 뽑을개수 중복혀용) 입력해주세요\nex) 2 9 3 X (대문자 주의)',color=discord.Color.blue())
        await ctx.send(embed=embed)

        def checkAnswer(message):
            return message.author==ctx.author and message.channel==ctx.channel

        while True:
            message=await self.client.wait_for("message",check=checkAnswer)
            lst=message.content.split(' ')

            if lst[-1]=='X' and (int(lst[1])-int(lst[0])<int(lst[2])):
                pass
            else:
                break

            embed=discord.Embed(title='오류 발생',description='범위를 확인해주세요',color=discord.Color.red())
            await ctx.send(embed=embed)

        num=''
        while len(num)<2*int(lst[2]):
            a=randint(int(lst[0]),int(lst[1]))
            if lst[-1]=='O':
                num+=str(a)+' '
            else:
                if str(a) not in num:
                    num+=str(a)+' '

        embed=discord.Embed(title='결과',description=num,color=discord.Color.blue())
        await ctx.send(embed=embed)
#--------------------------------------------------------------   
def setup(client):
    client.add_cog(Random(client))
            
