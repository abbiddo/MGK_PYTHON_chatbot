import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import asyncio

class Lastspell(commands.Cog):
    def __init__(self, client):
        self.client = client
#--------------------------------------------------------------
    @commands.command(name='끝말잇기')
    async def _끝말잇기(self,ctx):
        embed=discord.Embed(title='끝말잇기',description='끝말잇기를 시작할게요! 먼저 입력해주세요!\n첫 단어로 끝내기 없기! 그럼 반칙패!!',color=discord.Color.blue())
        await ctx.send(embed=embed)

        wordList=[]
        
        def checkMessage(message):
            return message.author==ctx.author and message.channel==ctx.channel

        def findword(spell):
            #네이버 국어사전 이 놈 자식...ㅡ.ㅡ
            url='https://dic.daum.net/search.do?q=%s로 시작하는 단어&dic=kor'%spell
            raw=requests.get(url)
            soup=BeautifulSoup(raw.text,"html.parser")
            box=soup.find('div',{'class':'search_box'})
            
            if box==None:
                return '없음'
            
            words=box.find_all('a',{'class':'txt_searchword'})
            
            for i in words:
                word=i.text
                if i.text[-1].isdigit():
                    word=i.text[0:len(i.text)-1]
                if len(i.text)>1 and word not in wordList:
                    wordList.append(word)
                    return word

        def wordCorrect(wword):
            url='https://stdict.korean.go.kr/search/searchResult.do?pageSize=10&searchKeyword=%s'%wword
            raw=requests.get(url)
            soup=BeautifulSoup(raw.text,"html.parser")
            box=soup.find('span',{'class':'t_blue2'})
            
            if box==None:
                return '미등록'
            else:
                return '등록'
            
        answer=''
                    
        try:
            message=await self.client.wait_for("message",timeout=15.0,check=checkMessage)

            answer=findword(message.content[-1])
            wordList.append(message.content)
            
            if answer=='없음':
                embed=discord.Embed(title='패',description="반칙패!!!",color=discord.Color.red())
                await ctx.send(embed=embed)
                raise commands.CommandError('GameOver')

            correct=wordCorrect(message.content)

            if correct=='미등록':
                embed=discord.Embed(title='패',description="사전에 등재되지 않은 단어입니다",color=discord.Color.red())
                await ctx.send(embed=embed)
                raise commands.CommandError('GameOver')
            
        except asyncio.TimeoutError:
            embed=discord.Embed(title='땡! 시간초과',description="명령어를 다시 입력하세요",color=discord.Color.red())
            await ctx.send(embed=embed)
            raise commands.CommandError('TimeOver') 

        await ctx.send('%s'%answer)
        
        cnt=0
        while True:
            try:
                message=await self.client.wait_for("message",timeout=5.0,check=checkMessage)

                if message.content[0]!=answer[-1]:
                    embed=discord.Embed(title='패',description="끝말이 이어지지 않습니다!",color=discord.Color.red())
                    await ctx.send(embed=embed)
                    raise commands.CommandError('GameOver')
                
                if message.content in wordList:
                    embed=discord.Embed(title='패',description="중복 단어 입니다!!!",color=discord.Color.red())
                    await ctx.send(embed=embed)
                    raise commands.CommandError('GameOver')

                correct=wordCorrect(message.content)

                if correct=='미등록':
                    embed=discord.Embed(title='패',description="사전에 등재되지 않은 단어입니다",color=discord.Color.red())
                    await ctx.send(embed=embed)
                    raise commands.CommandError('GameOver')

                answer=findword(message.content[-1])
                wordList.append(message.content)
                
                if answer=="없음":
                    embed=discord.Embed(title='승',description="승리하셨습니다!",color=discord.Color.blue())
                    await ctx.send(embed=embed)
                    raise commands.CommandError('Win') 
                
            except asyncio.TimeoutError:
                embed=discord.Embed(title='패',description="시간초과 되었습니다",color=discord.Color.red())
                await ctx.send(embed=embed)
                raise commands.CommandError('TimeOver') 

            await ctx.send('%s'%answer)
#--------------------------------------------------------------
def setup(client):
    client.add_cog(Lastspell(client))
