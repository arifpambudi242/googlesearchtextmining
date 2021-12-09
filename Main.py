import requests
from bs4 import BeautifulSoup as bs
from nltk.corpus import stopwords
import re

positive_words = [w.strip('\n')
                  for w in open('positive-words.txt', 'r').readlines()]
negative_words = [w.strip('\n')
                  for w in open('negative-words.txt', 'r').readlines()]


class SentimentAnalisys:
    def __init__(self, positive_words, negative_words):
        self.__positive_words = positive_words
        self.__negative_words = negative_words

    def getSentiment(self, keyword):
        urls = self.getUrls(keyword)
        articles = self.getArticles(urls)
        return 'Positive' if self.sentiment(articles) else 'Negative'

    def getUrls(self, keyword):
        print('Looking for Url.....')
        listUrl = []
        for x in range(5):
            link = "https://google.com/search?q=%s&tbm=nws&source=web&lr=lang_en&start=%s" % (
                keyword, x)
            with requests.Session() as s:
                try:
                    html = s.get(link)
                    soup = bs(html.text, 'html.parser')
                    h = soup.find_all(['a'])
                    for tag in h:
                        url = tag.get('href')
                        if 'http' in url and 'google.' not in url and 'youtube.' not in url:
                            # getting url
                            url = tag.get('href')
                            # check sparator
                            sparator = url.split('http')[0]
                            if sparator != '':
                                listUrl.append('%s' % url.split(sparator)[
                                               1].split('&')[0].split('%3')[0])
                        else:
                            continue
                except:
                    continue
        return listUrl

    def getArticles(self, listUrl=None):
        print('Getting Articles.....')
        listArticle = []
        try:
            for url in listUrl:
                with requests.Session() as s:
                    html = s.get(url)
                    if 'article' in html.text:
                        soup = bs(html.text, 'html.parser')
                        hasil = soup.find_all(['article'])
                        for h in hasil:
                            if h.text.strip() != '' and h.text.strip() != '\n':
                                listArticle.append(h.text.strip().lower())
                    else:
                        continue
            print('{} articles found'.format(len(listArticle)))
            joinedArticle = ' '.join(listArticle)
            # validating character
            validArticle = re.sub("[^A-Za-z0-9" "]+", " ", joinedArticle)
            wordArticle = validArticle.split(' ')
            return [w for w in wordArticle if not w in stopwords.words('english')]
        except Exception as e:
            return False

    def sentiment(self, articles):
        print('getting sentiment from {} words'.format(len(articles)))
        negative = 0
        positive = 0
        for text in articles:
            if text in self.__positive_words:
                positive += 1
            if text in self.__negative_words:
                negative += 1
        return positive > negative


def main():
    global positive_words
    global negative_words
    sentiment = SentimentAnalisys(positive_words, negative_words)

    print(sentiment.getSentiment('sesuatu'))


if __name__ == '__main__':
    main()
