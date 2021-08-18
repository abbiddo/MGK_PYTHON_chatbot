from discord.ext import commands
import discord

class Guid(commands.Cog):
    def __init__(self, client):
        self.client = client
#--------------------------------------------------------------        
    @commands.command(name='가이드')
    async def _가이드(self,ctx):
        embed=discord.Embed(title='가이드',description="흥챗봇에서 사용할 수 있는 명령어에 대한 설명입니다.",color=0xffc0cb)
        embed.add_field(name="!가이드",value="흥챗봇에 대한 가이드를 보여줍니다",inline=False)
        embed.add_field(name="!ping",value="pong:을 출력해주는 귀여운 기능입니다",inline=False)
        embed.add_field(name="!이름",value="명령어를 입력한 사용자의 닉네임을 출력합니다",inline=False)
        embed.add_field(name="!날짜",value="오늘 날짜를 출력합니다",inline=False)
        embed.add_field(name="!시간",value="현재 시간을 초단위로 출력합니다",inline=False)
        embed.add_field(name="!점심추천 (한식)",value="오늘의 점심 메뉴를 추천해줍니다\n!점심추천 뒤에 원하는 카테고리를 최대 두 개 입력할 수 있습니다",inline=False)
        embed.add_field(name="!퀴즈",value="봇이 넌센스 퀴즈를 출제합니다\n사용자의 닉네임으로 점수 집계를 합니다",inline=False)
        embed.add_field(name="!랭킹",value="퀴즈에 대한 점수와 랭킹을 알려줍니다.\n봇 재실행 시 점수는 초기화 됩니다.",inline=False)
        embed.add_field(name="!날씨 (시 군/구 동)",value="오늘의 기온, 체감온도, 미세먼지 등을 알려줍니다\n!날씨 명령어와 함께 원하는 위치를 입력해야 합니다\n시 군/구 동 중 최소 한 개, 순서는 지켜야합니다.",inline=False)
        embed.add_field(name="!코로나",value="전 날 코로나 확진자와 누적 확진자 수를 알려줍니다",inline=False)
        await ctx.send(embed=embed)
#--------------------------------------------------------------
    
def setup(client):
    client.add_cog(Guid(client))
