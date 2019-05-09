from bs4 import BeautifulSoup 
from requests import get
j = "https://maldivestimes.com/?s="+'--x'
all_links=[]
cols=[ "authors",'date_publish','description','text','title','url']
maldivestimes_data=pd.DataFrame(columns=cols)
for i in ['drugaddicts','narcotics','alcoholicsanonymous','rehabilitation','alcohol','abuse','drinking','sober',
         'gamblers','foodaddicts','recovery','foodaddiction']:
    url = j.replace('--x',i) # replace it with a url you want to apply the rules to  
    soup = BeautifulSoup(get(url).text, 'lxml')   
    for i in range(len(soup.find_all('h2',attrs={'class':"entry-title"}))):
        all_links.append(soup.find_all('h2',attrs={'class':"entry-title"})[i].a['href'])

for i in all_links:
    article = NewsPlease.from_url(i)
    maldivestimes_data.loc[len(maldivestimes_data)]=[article.authors,article.date_publish,article.description,
                                             article.text,article.title,article.url]

maldivestimes_data.to_csv('Maldivestimes.csv',index=True)
