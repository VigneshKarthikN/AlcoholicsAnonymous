from selenium.webdriver.chrome.options import Options # enables options in web browser
from selenium import webdriver # web-based automation tool for Python
from newspaper import Article # Article scraping & curation
from bs4 import BeautifulSoup # Python library for pulling data out of HTML and XML files
from requests import get # standard for making HTTP requests in Python
import pandas as pd # library written for data manipulation and analysis
import sys, time #  System-specific parameters and functions

headlines, descriptions, dates, authors, news, keywords, summaries, urls = [], [], [], [], [], [], [], []

keyword = 'Alcoholics Anonymous site:kathmandupost.ekantipur.com'

url = 'https://www.google.com/search?q=' + '+'.join(keyword.split())
print(url)
options = Options()
options.headless = True
browser = webdriver.Chrome(options=options)
browser.get(url)

page = browser.page_source
soup = BeautifulSoup(page, 'lxml')
max_pages = round([int(s) for s in soup.select_one('#resultStats').text.split() if s.isdigit()][0]/10)
print(max_pages)

index = 0

while True:
    try:
        index +=1
        page = browser.page_source
        soup = BeautifulSoup(page, 'lxml')
        linky = [soup.select('.r')[i].a['href'] for i in range(len(soup.select('.r')))]
        urls.extend(linky)
        print(index)
        if index == max_pages:
            break
        browser.find_element_by_xpath('//*[@id="pnnext"]/span[2]').click()
        time.sleep(2)
        sys.stdout.write('\r' + str(index) + ' : ' + str(max_pages) + '\r')
        sys.stdout.flush()
    except:
        pass
    
browser.quit()

urls = list(dict.fromkeys(urls))
print(len(urls), type(urls))

for index, url in enumerate(urls):
    try:
        # Parse the url to NewsPlease 
        soup = BeautifulSoup(get(url).text, 'lxml')
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        
        # Extracts the Headlines
        try:
            try:
                headlines.append(article.title.strip())
            except:
                headlines.append(soup.select_one('meta[property="og:title"]')['content'].strip())
        except:
            headlines.append(None)
            
        # Extracts the Descriptions    
        try:
            try:
                descriptions.append(soup.select_one('meta[property="og:description"]')['content'].strip().replace('\n', ' '))
                
            except:
                descriptions.append(article.meta_description.strip())
        except:
            descriptions.append(None)
            
        # Extracts the Authors
        try:
            try:
                authors.append(soup.select_one('meta[name="author"]')['content'].strip())
            except:
                authors.append(article.authors.strip())
        except:
            authors.append(None)
        
        # Extracts the published dates
        try:
            try:
                dates.append(soup.select_one('meta[property="article:published_time"]')['content'].strip())
            except:
                dates.append(str(article.publish_date))
        except:
            dates.append(None)
            
        # Extracts the news articles
        try:
            try:
                news.append(soup.select_one('.storyText').text.replace('\n', '').strip())
            except:
                news.append(article.text.strip())
        except:
            news.append(None)
            
        # Extracts Keywords and Summaries    
        try:
            keywords.append(article.keywords)
            summaries.append(article.summary)
        except:
            keywords.append(None)
            summaries.append(None)
            
    except:
        headlines.append(None)
        descriptions.append(None)
        authors.append(None)
        dates.append(None)
        news.append(None)
        keywords.append(None)
        summaries.append(None)

    sys.stdout.write('\r' + str(index) + ' : ' + str(url) + '\r')
    sys.stdout.flush()

tbl = pd.DataFrame({'Headlines' : headlines,
                    'Descriptions' : descriptions,
                    'Authors' : authors,
                    'Published_Dates' : dates, 
                    'Articles' : news,
                    'Keywords' : keywords,
                    'Summaries' : summaries,})
#tbl = tbl.dropna()
tbl.to_csv('Katmandu.csv', index=False)
tbl.head()
