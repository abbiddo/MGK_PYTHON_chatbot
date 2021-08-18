import asyncio
import discord
from discord.ext import commands
import csv
import json
from random import *

class Quiz(commands.Cog):
    def __init__(self, client):
        self.client=client
        self.quizDict={}
        self.scoreDict={}

        with open("./data/quiz.csv","r",encoding="utf-8") as f:
            reader=csv.reader(f)
            for row in reader:
                self.quizDict[row[0]]=row[1]

#--------------------------------------------------------------        
    @commands.command(name = "퀴즈")
    async def _quiz(self,ctx):
        problemList=list(self.quizDict.keys())
        problem=choice(problemList)
        answer=self.quizDict[problem]
        embed=discord.Embed(title='퀴즈',description=problem,color=discord.Color.blue())
        await ctx.send(embed=embed)

        def checkAnswer(message):
            if message.channel==ctx.channel and answer in message.content:
                return True
            else:
                return False
        try:
            message=await self.client.wait_for("message",timeout=10.0,check=checkAnswer)
            name=message.author.name
            
            with open("data/score.json", 'r', encoding='utf-8') as f:
                self.scoreDict = json.load(f)
        
            if message.author.name in self.scoreDict:
                self.scoreDict[message.author.name]+=1
            else:
                self.scoreDict[message.author.name]=1
                    
            with open("data/score.json","w",encoding="utf-8") as f:
                json.dump(self.scoreDict,f,ensure_ascii=False)

            embed=discord.Embed(title='',description="%s님, 정답이에요!"%(name),color=discord.Color.blue())
            await ctx.send(embed=embed)

        except asyncio.TimeoutError:
            embed=discord.Embed(title='',description="땡! 시간초과예요!\n답은 %s 입니다"%answer,color=discord.Color.red())
            await ctx.send(embed=embed)
#-------------------------------------------------------------- 
    @commands.command(name = "랭킹")
    async def _rank(self,ctx,nameList=[]):
        with open("data/score.json", 'r', encoding='utf-8') as f:
            self.scoreDict = json.load(f)
        score = sorted(self.scoreDict.items(), key = lambda x : x[1])
        
        if len(nameList)==0:
            if len(self.scoreDict)==0:
                embed=discord.Embed(title="",description="아무도 퀴즈에 참여하지 않았습니다.",color=discord.Color.red())

            else:
                embed=discord.Embed(title='랭킹',description="퀴즈 랭킹입니다.\n문제를 맞출 때 마다 1점씩 증가해요!",color=0xffd700)
                for i in range(len(score)-1,-1,-1):
                    embed.add_field(name="%s. %s"%(len(score)-i,score[i][0]),value="점수 : %s"%score[i][1],inline=False)
            
                if ctx.author.name not in self.scoreDict:
                    embed.add_field(name='ㅤ',value="%s님은 퀴즈에 참여하지 않았습니다. 퀴즈에 도전하세요!"%ctx.author.name)

                else:                
                    if ctx.author.name==score[-1][0]:
                        embed.add_field(name='ㅤ',value="축하합니다! %s님은 현재 1등입니다!"%ctx.author.name)

                    else:
                        for i in range(len(score)-1,-1,-1):
                            a=i
                            if score[i][0]==ctx.author.name:
                                break
                        embed.add_field(name='ㅤ',value="%s님은 현재 %s등입니다!\n%s등과 점수차는 %s점입니다"%(ctx.author.name,len(score)-a,len(score)-a-1,score[a+1][1]-score[a][1]))
            await ctx.send(embed=embed)

        else:
            name=''
            for i in range(len(nameList)):
                name=name+nameList[i]

            embed=discord.Embed(title='개인 퀴즈 랭킹',description='개인 퀴즈 랭킹입니다,',color=0xffd700)
            if name in self.scoreDict:
                for i in range(len(score)-1,-1,-1):
                    a=i
                    if score[i][0]==name:
                        break
                embed.add_field(name='%s'%name,value="%s님은 현재 %s점으로 %s등입니다!"%(name,self.scoreDict[name],len(score)-a))

            else:
                embed.add_field(name='%s'%name,value="%s님은 퀴즈에 참여하지 않았습니다."%name)
            await ctx.send(embed=embed)
#--------------------------------------------------------------   
def setup(client):
    client.add_cog(Quiz(client))
