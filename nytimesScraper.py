import requests
import pprint
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=4)

class Article:

	def __init__(self, url=None) -> None:
		self.url = url
		self.raw = None
		self.data = {}
	
	def getInfo(self):
		return self.data

	def scrape(self):
		if not self.url:
			raise Exception("Article url seems to be empty. Try passing it via the constructor!")
		response = requests.get(self.url)
		if response.status_code != 200:
			raise Exception("Something wen't wrong! Couldn't download article")
		self.raw = response.content

	def parse(self):
		soup = BeautifulSoup(self.raw, 'html.parser')
		self.data["Heading"] = soup.h1.string
		self.data["Author"] = soup.find(itemprop="name").get_text()
		self.data["PublishedAt"] = soup.time.get_text()
		paragraphs = []
		for paragraph in soup.find_all(attrs={'class':"css-axufdj evys1bk0"}):
			paragraphs.append(paragraph.get_text())
		self.data["Content"] = paragraphs

if __name__ == "__main__":
	nyTimes = Article(url='https://www.nytimes.com/2021/08/07/sports/olympics/covid-closing-ceremony-athletes.html')
	# Retreive the Article
	nyTimes.scrape()
	# Extract Required Information
	nyTimes.parse()
	# Pretty Print
	pp.pprint(nyTimes.getInfo())
