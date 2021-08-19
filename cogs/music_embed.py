import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class Musice(commands.Cog):
    def __init__(self,client):
        option={'format':'bestaudio/best','noplaylist':True,}
        self.client=client
        self.DL=YoutubeDL(option)
#-------------------------------------------------------------- 
    @commands.command(name="유튜브")
    async def play_musice(self,ctx,url=None):
        if url==None:
            embed=discord.Embed(title='오류 발생',description='음악을 재생할 url을 입력해주세요',color=discord.Color.red())
            await ctx.send(embed=embed)
            raise commands.CommandError("'Url' is a required element.")
            
        if 'https://youtu.be/' not in url and 'https://www.youtube.com/' not in url:
            embed=discord.Embed(title='오류 발생',description='youtube url을 입력해주세요',color=discord.Color.red())
            await ctx.send(embed=embed)
            raise commands.CommandError("'Url' is not youtube url")
        
        data=self.DL.extract_info(url,download=False)
        embed=discord.Embed(title=data['title'],url=url,color=discord.Color.red())
        embed.set_author(name=data['uploader'],url=data['url'])
        embed.add_field(name='조회수',value=data['view_count'],inline=True)
        embed.add_field(name='좋아요 수',value=data['like_count'],inline=True)
        embed.add_field(name='업로드 날짜',value=data['upload_date'],inline=True)
        embed.set_image(url=data['thumbnail'])
        await ctx.send(embed=embed)
#-------------------------------------------------------------- 
def setup(client):
    client.add_cog(Musice(client))
