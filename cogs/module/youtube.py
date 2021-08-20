# 사용 X
# 모각코에서 준 모듈 / music 파일에 직접 사

import requests
#import urllib.parse
import json

def getUrl(keyword):

# 한글로 입력한 검색어를 주소형식으로 인코딩하고 기본 url에 키워드 넣기
#    encoded_search = urllib.parse.quote_plus(keyword)
    url = f"https://www.youtube.com/results?search_query={encoded_search}&sp=EgIQAQ%253D%253D"
    response = requests.get(url).text
    while "ytInitialData" not in response:
        response = requests.get(url).text
    
# 이 요소가 뭔지 정확히 알 진 못했지만 정보를 다 담고 있는 딕셔너리의 키 같음 
# 이 요소의 위치 + 요소의 길이 + 3 / 뒤에 3을 해주는 이유는 코드 밖에서 설명
    start = (response.index("ytInitialData")+len("ytInitialData")+3) # ' = '

# start이후로 '};' 가 나오는 부분을 찾고 인덱스로 활용할 것이니 +1
    end = response.index("};", start) + 1
    
# start ~ end json에 저장
    json_str = response[start:end]
    data = json.loads(json_str)

# 이게 어떤 거다! 라고 설명하긴 그렇지만 저장한 json 파일을 타고타고 들어가서 필요한 정보까지 도달하는 코드
    videos = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
        "sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
        
# videos의 첫번째 인덱스에서 또 타고타고 들어가서 유튜브 주소를 생성해 반환
# 반복문이지만 첫 반복에 return을 해버리므로 반복문은 한번만 실행
    for row in videos:
        video_data = row.get("videoRenderer", {})
        duration = str(video_data.get("lengthText", {}).get("simpleText", 0))
        return "https://www.youtube.com/" +video_data.get("navigationEndpoint", {}).get("commandMetadata", {}).get("webCommandMetadata", {}).get("url", None)
