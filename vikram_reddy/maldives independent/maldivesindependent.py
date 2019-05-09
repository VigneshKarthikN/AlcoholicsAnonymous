from bs4 import BeautifulSoup 
from requests import get
all_links=[]
cols=[ "authors",'date_publish','description','text','title','url']
maldivesindependent_data=pd.DataFrame(columns=cols)
j = 'https://maldivesindependent.com/?s='+'--x'
for i in ['drugaddicts','narcotics','alcoholicsanonymous','rehabilitation','alcohol','abuse','drinking','sober',
         'gamblers','foodaddicts','recovery','foodaddiction']:
    url = j.replace('--x',i) # replace it with a url you want to apply the rules to  
    print(url)
    soup = BeautifulSoup(get(url).text, 'lxml')
    for i in range(len(soup.find_all('li',attrs={'class':"mvp-blog-story-wrap left relative infinite-post"}))):
        all_links.append(soup.find_all('li',attrs={'class':"mvp-blog-story-wrap left relative infinite-post"})[i].a['href'])
from newsplease import NewsPlease
for i in all_links:
    article = NewsPlease.from_url(i)
    maldivesindependent_data.loc[len(maldivesindependent_data)]=[article.authors,article.date_publish,article.description,
                                             article.text,article.title,article.url]
maldivesindependent_data.to_csv('maldivesindependent.csv',index=True)