from discord.ext import commands
import discord

class Example(commands.Cog):
    def __init__(self, client):
        self.client = client

#--------------------------------------------------------------        
    @commands.command(name = "ping")
    async def _ping(self,ctx):
        embed=discord.Embed(title='pong!',color=0xa9a9a9)
        await ctx.send(embed=embed)
#--------------------------------------------------------------
    @commands.command(name='이름')
    async def _이름(self,ctx):
        embed=discord.Embed(title="명령어를 입력하신 분의 이름은 "+ctx.author.name+" 입니다",color=0xa9a9a9)
        await ctx.send(embed=embed)
#--------------------------------------------------------------
  
    
def setup(client):
    client.add_cog(Example(client))
