import asyncio
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
import requests
import json

class Music(commands.Cog):
    def __init__(self,client):
        option={'format':'bestaudio/best','noplaylist':True,}
        self.client=client
        self.DL=YoutubeDL(option)
#-------------------------------------------------------------- 
    @commands.command(name="음악재생")
    async def play_music(self,ctx,*keywords):
        
        if len(keywords)==0:
            embed=discord.Embed(title='오류 발생',description='검색어를 입력해주세요',color=discord.Color.red())
            await ctx.send(embed=embed)
            raise commands.CommandError("'keywords' is a required element.")

# 링크 입력이 아니므로 유튜브 링크가 아닐 때 발생시켰던 오류 코드 삭제

        if ctx.voice_client is None: # 봇이 음성 채널애 연결되어 있지 않으면
            if ctx.author.voice: # 명령어 작성자의 음성 채널 연결 상태
                await ctx.author.voice.channel.connect() # 봇을 명령어 작성자가 있는 음성 채널에 연결

            else:
                embed=discord.Embed(title='오류 발생',description='음성 채널에 들어간 후 명령어를 사용해 주세요!',color=discord.Color.red())
                await ctx.send(embed=embed)
                raise commands.CommandError("Author not connedcted to a voice channel.") # 이후 코드를 실행하지 않기 위해 raise 사용

        elif ctx.voice_client.is_playing(): # 봇이 음성 채널에 연결되어 있고, 재생중이라면
            ctx.voice_client.stop() # 재생중인 음원 종료

        embed=discord.Embed(title='목록 검색 중',description='잠시만 기다려 주세요',color=0xffd770)
        await ctx.send(embed=embed)

# 오늘 공부한 부분인데 저는 키워드를 *로 안받고 그냥 리스트로 받았기 때문에
# 리스트를 문자열로 바꿔주는 작업
        keyword=''
        for i in keywords:
            keyword=keyword+i

# 여기가 원래 모듈 코드 / 검색한 화면의 여러 영상들에 대한 정보를 json에 저장
        url="https://www.youtube.com/results?search_query=%s"%keyword
        response = requests.get(url).text
        
        while "ytInitialData" not in response:
            response = requests.get(url).text

        start = (response.index("ytInitialData")+len("ytInitialData")+3) # ' = '
        end = response.index("};", start) + 1    
    
        json_str = response[start:end]
        data = json.loads(json_str)

        videos = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
            "sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]

        embed=discord.Embed(title='%s 목록'%keyword,description='해당 검색어의 검색 목록입니다.\n번호를 입력해주세요',color=0xffd700)

# 모듈과 짬뽕된 코드로 for문 안의 두 줄로 링크에 필요한 요소들을 뽑고
# 링크를 완성한 후에 그 링크 영상의 정보를 가져와 embed에 내용추가
# 그리고 링크를 리스트에 저장
# 5번만 반복
        a=0
        url_lst=[]
        for row in videos:
            video_data = row.get("videoRenderer", {})
            duration = str(video_data.get("lengthText", {}).get("simpleText", 0))
            urls="https://www.youtube.com/"+video_data.get("navigationEndpoint", {}).get("commandMetadata", {}).get("webCommandMetadata", {}).get("url", None)
            data2=self.DL.extract_info(urls,download=False)
            embed.add_field(name="%d"%(a+1),value="%s"%(data2['title']),inline=False)
            a+=1
            url_lst.append(urls)
            if a==5:
                break

        await ctx.send(embed=embed)

# 몇 번 째 영상을 재생할건지 입력하면 퀴즈처럼 티키타카 하는 코드 
        def checkAnswer(message):
            if message.channel==ctx.channel:
                return True
            else:
                return False
            
        n=0
        try:
            while True:
                n=await self.client.wait_for("message",timeout=60.0,check=checkAnswer)
                if n.content.isdigit() and int(n.content)>0 and int(n.content)<6:
                    await ctx.send(url_lst[int(n.content)-1])
                    embed=discord.Embed(title='음악 재생',description='음악 재생을 준비하고 있어요. 잠시만 기다려 주세요!',color=0xffd700)
                    await ctx.send(embed=embed)
                    break

                embed=discord.Embed(title='오류 발생',description='번호를 잘못 입력하셨습니다\n목록에 있는 숫자만 입력해주세요',color=discord.Color.red())
                await ctx.send(embed=embed)
                        
                
        except asyncio.TimeoutError:
            embed=discord.Embed(title='시간초과',description="명령어를 다시 입력하세요",color=discord.Color.red())
            await ctx.send(embed=embed)

        data=self.DL.extract_info(url_lst[int(n.content)-1],download=False)
        link=data['url']
        title=data['title']

        ffmpeg_options={'options':'-vn', 'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}
        # 비디오 사용 X, ffmpeg에서 연결이 끊기는 경우 재연결 시도
        player=discord.FFmpegPCMAudio(link,**ffmpeg_options,executable="C:/ffmpeg/bin/ffmpeg")
        ctx.voice_client.play(player)
        
        embed=discord.Embed(title='음악재생',description='%s 재생을 시작할게요'%title,color=discord.Color.blue())
        await ctx.send(embed=embed)
#--------------------------------------------------------------
    @commands.command(name="음악종료")
    async def quit_music(self,ctx):
        voice=ctx.voice_client
        if voice.is_connected():
            await voice.disconnect()
            embed=discord.Embed(title='',description='음악 재생을 종료합니다',color=discord.Color.red())
            await ctx.send(embed=embed)
#--------------------------------------------------------------
    @commands.command(name="일시정지")
    async def pause_music(self,ctx):
        voice=ctx.voice_client
        if voice.is_playing():
            voice.pause()
            embed=discord.Embed(title='',description='음악 재생을 일시정지합니다',color=0xffd770)
            await ctx.send(embed=embed)
#--------------------------------------------------------------
    @commands.command(name="다시시작")
    async def resume_music(self,ctx):
        voice=ctx.voice_client
        if voice.is_paused():
            voice.resume()
            embed=discord.Embed(title='',description='음악을 다시 재생합니다',color=discord.Color.blue())
            await ctx.send(embed=embed)
#-------------------------------------------------------------- 
def setup(client):
    client.add_cog(Music(client))
