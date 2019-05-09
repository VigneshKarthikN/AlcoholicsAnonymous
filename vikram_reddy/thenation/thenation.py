from bs4 import BeautifulSoup 
from requests import get
all_links=[]
cols=[ "authors",'date_publish','description','text','title','url']
thenation_data=pd.DataFrame(columns=cols)
j='https://www.thenation.com/?ssearch='+'--x'+'&post_type=article'
#print(j)
for i in ['drugaddicts','narcotics','alcoholicsanonymous','rehabilitation','alcohol','abuse','drinking','sober',
         'gamblers','foodaddicts','recovery','foodaddiction']:
    url = j.replace('--x',i) # replace it with a url you want to apply the rules to  
    print(url)
    soup = BeautifulSoup(get(url).text, 'lxml')

    links = [soup.select('div.details')[i].h3.a['href'] for i in range(len(soup.select('div.details')))]
    all_links.append(links)
all_links1=[i for j in all_links for i in j]
from newsplease import NewsPlease
for i in all_links1:
    article = NewsPlease.from_url(i)
    thenation_data.loc[len(thenation_data)]=[article.authors,article.date_publish,article.description, article.text,article.title,article.url]
thenation_data.to_csv('thenation_data.csv',index=True)