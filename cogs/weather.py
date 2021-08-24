from discord.ext import commands
import discord
import requests
from bs4 import BeautifulSoup

class Weather(commands.Cog):
    def __init__(self, client):
        self.client = client
#--------------------------------------------------------------        
    @commands.command(name='날씨')
    async def _날씨(self,ctx,*area):
        if len(area)==0:
            embed=discord.Embed(title='날씨',description="'!날씨'와 함께 시, 군/구, 동을 입력하세요\nex) !날씨 서울, !날씨 서울 여의도동, !날씨 서울 여등포구 여의도동",color=0x87cefa)
            await ctx.send(embed=embed)
        else:
            area='%s'%(' '.join(area))
            url='https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%s날씨'%area

            raw=requests.get(url)
            soup=BeautifulSoup(raw.text,"html.parser")
            box=soup.find('div', {'class' : 'today_area _mainTabContent'})
            temp=box.find_all('span',{'class':'todaytemp'})
            temps=box.find_all('span',{'class':'num'})
            dust=box.find_all('dd')
            feel=box.find_all('p',{'class':'cast_txt'})
            sense=box.find('span',{'class':'sensible'})
            sensetemp=sense.find_all('em')

            embed=discord.Embed(title='날씨',description='오늘 %s의 날씨에 대한 정보입니다.'%area,color=0x87cefa)
            embed.add_field(name='현재온도',value='현재온도는 %s°로 %s'%(temp[0].text,feel[0].text),inline=False)
            embed.add_field(name='기온',value='체감온도 : %s°\n최저기온 : %s°, 최고기온 :  %s°'%(sensetemp[0].text,temps[0].text,temps[1].text),inline=False)
            embed.add_field(name='미세먼지',value="미세먼지는 %s, 초미세먼지는 %s입니다"%(dust[0].text,dust[1].text),inline=False)
            await ctx.send(embed=embed)
#--------------------------------------------------------------
def setup(client):
    client.add_cog(Weather(client))
