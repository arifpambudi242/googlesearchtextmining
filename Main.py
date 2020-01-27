#!Env/bin/python
import requests
from bs4 import BeautifulSoup as bs
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import re
import sys

fileSentences = open('hasil.txt', 'w')
stopword = open('stopword.txt', 'r').read()
stopword = stopword.split('\n')




# Main program
def main():
	keyword = 'Virus Corona'
	url = cariUrl(keyword)
	print('ditemukan %s link'%url['jumlah'])
	if url['jumlah'] > 0:
		hasil = grabArticle(url['urls'])
		buatHasil(hasil)
		buatPlot(hasil)
	else:
		print('tidak ada link apapun!')
		sys.exit()




# menemukan link article di search engine google
def cariUrl(keyword=None):
	print('Cari Url.....')
	listUrl = []
	for x in range(3):
		link = "https://google.com/search?q=%s&start=%s"%(keyword,x)
		with requests.Session() as s:
			html = s.get(link)

			soup = bs(html.text, 'html.parser')

			h = soup.find_all(['a'])

			for tag in h:
				url = tag.get('href')
				if 'http' in url:
					# ambil url
					url = tag.get('href')
					# check sparator
					sparator = url.split('http')[0]
					if sparator != '':
						listUrl.append('%s'%url.split(sparator)[1].split('&')[0])
				else:
					continue
	return {'urls': listUrl, 'jumlah': len(listUrl)}


def grabArticle(listUrl=None):
	print('Grabbing Article.....')
	listArticle = []
	try:
		for url in listUrl:
			with requests.Session() as s:
				html = s.get(url)
				soup = bs(html.text, 'html.parser')
				hasil = soup.find_all(['p'])
				for h in hasil:
					if h.text.strip() != '':
						listArticle.append(h.text.strip().lower())
		joinedArticle = ' '.join(listArticle)
		# check ke validan karakter
		validArticle = re.sub("[^A-Za-z0-9" "]+", " " , joinedArticle)

		wordArticle = validArticle.split(' ')

		validwordArticle = [w for w in wordArticle if not w in stopword]

		return ' '.join(validwordArticle)
	except:
		pass


def buatHasil(sentences=None):
	print('Post Hasil to file!!.....')
	fileSentences.write(sentences)
	# for sentence in sentences:
	# 	fileSentences.write(sentence+'\n')
	fileSentences.close()

	return '!done'

def buatPlot(kata=None):
	print('Generating Article!.....')
	wordcloud = WordCloud(width=800, height=800, max_words=100, background_color='white').generate(kata)

	# Display the generated image:
	plt.imshow(wordcloud, interpolation='bilinear')
	plt.axis("off")
	plt.show()


if __name__ == '__main__':
	main()
