from newsplease import NewsPlease
from bs4 import BeautifulSoup 
from requests import get

j = 'https://en.sun.mv/search?q='+'--x'
all_links=[]
cols=[ "authors",'date_publish','description','text','title','url']
sun_data=pd.DataFrame(columns=cols)
for i in ['drugaddicts','narcotics','alcoholicsanonymous','rehabilitation','alcohol','abuse','drinking','sober',
         'gamblers','foodaddicts','recovery','foodaddiction']:
    url = j.replace('--x',i) # replace it with a url you want to apply the rules to  
    print(url)
    soup = BeautifulSoup(get(url).text, 'lxml')
    for i in range(len(soup.find_all('div',attrs={'class':"widget-article article-feetha article-feetha-search"}))):
        all_links.append(soup.find_all('div',attrs={'class':"widget-article article-feetha article-feetha-search"})[i].a['href'])
cols=[ "authors",'date_publish','description','text','title','url']
sun_data=pd.DataFrame(columns=cols)
for i in all_links:
    article = NewsPlease.from_url(i)
    sun_data.loc[len(sun_data)]=[article.authors,article.date_publish,article.description,
                                             article.text,article.title,article.url]
sun_data.to_csv('sun.csv',index=True)