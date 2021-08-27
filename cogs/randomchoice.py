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
    @commands.command(name = "추첨")
    async def _userchoice(self,ctx):
        embed=discord.Embed(title='당첨자 추첨',description='추첨에 참여하는 분들은 참여의사를 밝혀주세요\n마지막에 꼭 "끝"을 입력해주세요',color=discord.Color.blue())
        await ctx.send(embed=embed)

        def checkAnswer(message):
            return message.channel==ctx.channel

        person=[]
        while True:
            message=await self.client.wait_for("message",check=checkAnswer)
            if message.content=='끝':
                break
            if message.author.nick not in person:
                person.append(message.author.nick)

        embed=discord.Embed(title='당첨자 인원',description='몇 명을 추첨하실 건가요? (숫자만 입력해주세요)',color=discord.Color.blue())
        await ctx.send(embed=embed)

        while True:
            message=await self.client.wait_for("message",check=checkAnswer)
            
            if len(person)>int(message.content):
                break
            
            embed=discord.Embed(title='오류 발생',description='범위를 확인해주세요',color=discord.Color.red())
            await ctx.send(embed=embed)
            
        newper=''
        for i in range(int(message.content)):
            a=choice(person)
            person.remove(a)
            newper+=a+' '

        embed=discord.Embed(title='추첨 결과',description=newper,color=discord.Color.blue())
        await ctx.send(embed=embed)
#--------------------------------------------------------------
def setup(client):
    client.add_cog(Random(client))
            
