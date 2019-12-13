#메인페이지의 이미지 목록에서 이미지들 가져오기
#1.메인페이지를 가져오기
#2. 각 이미지 파일들을 요청해서 가져온다


#https://pixabay.com/ko/images/search/{검색키워드}/?pagi={페이지번호}

import os
import time
import requests
from bs4 import BeautifulSoup

def download_image_list(end_page=1,keyword=None):
    """pixabay 이미지 목록에 있는 사진들을 다운받는 함수

    keyword Arguments:
        end_page {int}--다운받을 목록의 마지막 페이지 (default:{1})
        keyword {str}--검색키워드 (default : {None})

    """
    # 이미지들을 저장할 디렉토리 생성
    dir='./pixabay_calli'
    if not os.path.isdir(dir):
        os.mkdir(dir)


    base_url='https://pixabay.com/ko/images/search/'  
    if keyword:
        base_url=base_url+keyword+'/'
    
    base_url=base_url+'?pagi={}'

    for page in range(1,end_page+1):
        url=base_url.format(page)
        print(url)
        res=requests.get(url)
        if res.status_code==200:
            soup=BeautifulSoup(res.text,'lxml')
        #selector:div.item
            img_tag_list=soup.select('div.item img')
            
            for img in img_tag_list:
                src_attr=img.get('src')
                if src_attr=='/static/img/blank.gif':
                    src_attr=img.get('data-lazy')
                
                    #이미지 파일명만 추출
                
                filename=dir+"/"+src_attr.split('/')[-1]

                #이미지 파일 요청 - 저장
                img_res=requests.get(src_attr)
                if img_res.status_code==200:
                    with open(filename,'wb') as f:
                        #binary 파일로 읽음
                        f.write(img_res.content)           
                else:
                    print("{}저장실패".format(filename))
                #다음 요청까지 간격
                time.sleep(0.5)

        else:
            print("페이지{} 요청실패".format(page))    





if __name__=='__main__':
    download_image_list(keyword='calligraphy',end_page=3)


        


    





