import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class Music(commands.Cog):
    def __init__(self,client):
        option={'format':'bestaudio/best','noplaylist':True,}
        self.client=client
        self.DL=YoutubeDL(option)
#-------------------------------------------------------------- 
    @commands.command(name="음악재생")
    async def play_music(self,ctx,url=None):
        if url==None:
            embed=discord.Embed(title='오류 발생',description='음악을 재생할 url을 입력해주세요',color=discord.Color.red())
            await ctx.send(embed=embed)
            raise commands.CommandError("'Url' is a required element.")
            
        if 'https://youtu.be/' not in url and 'https://www.youtube.com/' not in url:
            embed=discord.Embed(title='오류 발생',description='youtube url을 입력해주세요',color=discord.Color.red())
            await ctx.send(embed=embed)
            raise commands.CommandError("'Url' is not youtube url")
        
        if ctx.voice_client is None: # 봇이 음성 채널애 연결되어 있지 않으면
            if ctx.author.voice: # 명령어 작성자의 음성 채널 연결 상태
                await ctx.author.voice.channel.connect() # 봇을 명령어 작성자가 있는 음성 채널에 연결

            else:
                embed=discord.Embed(title='오류 발생',description='음성 채널에 들어간 후 명령어를 사용해 주세요!',color=discord.Color.red())
                await ctx.send(embed=embed)
                raise commands.CommandError("Author not connedcted to a voice channel.") # 이후 코드를 실행하지 않기 위해 raise 사용

        elif ctx.voice_client.is_playing(): # 봇이 음성 채널에 연결되어 있고, 재생중이라면
            ctx.voice_client.stop() # 재생중인 음원 종료
        await ctx.send(url)
        embed=discord.Embed(title='음악 재생',description='음악 재생을 준비하고 있어요. 잠시만 기다려 주세요!',color=0xffd700)
        await ctx.send(embed=embed)

        data=self.DL.extract_info(url,download=False)
        link=data['url']
        title=data['title']

        ffmpeg_options={'options':'-vn', 'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}
        # 비디오 사용 X, ffmpeg에서 연결이 끊기는 경우 재연결 시도
        player=discord.FFmpegPCMAudio(link,**ffmpeg_options,executable="C:/ffmpeg/bin/ffmpeg")

        ctx.voice_client.play(player)
        embed=discord.Embed(title='음악재생',description='%s 재생을 시작할게요'%title,color=discord.Color.blue())
        await ctx.send(embed=embed)
#--------------------------------------------------------------         
def setup(client):
    client.add_cog(Music(client))
