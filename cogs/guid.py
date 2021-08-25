from discord.ext import commands
import discord

class Guid(commands.Cog):
    def __init__(self, client):
        self.client = client
#--------------------------------------------------------------        
    @commands.command(name='가이드')
    async def _가이드(self,ctx):
        embed=discord.Embed(title='가이드',description="흥챗봇에서 사용할 수 있는 명령어에 대한 설명입니다.\n명령어는 '!'로 실행합니다",color=0xffc0cb)
        embed.add_field(name="!가이드",value="흥챗봇에 대한 가이드를 보여줍니다",inline=False)
        embed.add_field(name="!ping",value="pong:을 출력해주는 귀여운 기능입니다",inline=False)
        embed.add_field(name="!이름",value="명령어를 입력한 사용자의 닉네임을 출력합니다",inline=False)
        embed.add_field(name="!날짜",value="오늘 날짜를 출력합니다",inline=False)
        embed.add_field(name="!시간",value="현재 시간을 초단위로 출력합니다",inline=False)
        embed.add_field(name="!메뉴 (한식)",value="오늘의 메뉴를 추천해줍니다\n!메뉴 뒤에 원하는 카테고리를 최대 두 개 입력할 수 있습니다",inline=False)
        embed.add_field(name="!퀴즈",value="봇이 넌센스 퀴즈를 출제합니다\n사용자의 닉네임으로 점수 집계를 합니다",inline=False)
        embed.add_field(name="!랭킹",value="퀴즈에 대한 점수와 랭킹을 알려줍니다.\n봇 재실행 시 점수는 초기화 됩니다.",inline=False)
        embed.add_field(name="!날씨 (위치)",value="오늘의 기온, 체감온도, 미세먼지 등을 알려줍니다\n!날씨 명령어와 함께 원하는 위치를 입력해주세요",inline=False)
        embed.add_field(name="!코로나",value="전 날 코로나 확진자와 누적 확진자 수를 알려줍니다",inline=False)
        embed.add_field(name="!음악재생",value="유튜브에 검색어를 검색해 음원을 재생합니다\n음성채널을 연결하고 명령어를 입력하세요\n검색어를 함께 입력해주세요\n- !음악종료 : 음악을 종료합니다\n- !일시정지 : 음악을 일시 정지합니다.\n- !다시시작 : 음악을 다시 시작합니다.",inline=False)
        embed.add_field(name="!유튜브",value="유튜브 링크의 미리보기 embed를 출력합니다",inline=False)
        embed.add_field(name="!맛집 (지역 음식)",value="맛집을 검색합니다\n명령어와 함께 지역,음식을 입력하세요",inline=False)
        embed.add_field(name="!메뉴추천",value="메뉴 추천 후 맛집을 검색합니다\n명령어 입력 시 나오는 문구를 따라주세요",inline=False)

        await ctx.send(embed=embed)
#--------------------------------------------------------------
    
def setup(client):
    client.add_cog(Guid(client))
