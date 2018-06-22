"""	MARUMARU COLLECTOR	"""
"""	     	  BY IML  	"""
"""	shin10256|gmail.com   	"""	
"""	shino1025.blog.me    	"""
"""	github.com/iml1111   	"""	

from selenium import webdriver
from bs4 import BeautifulSoup
import re
import sys
import os
import img2pdf
import time
import requests

header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)\
			AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
			"Accept":"text/html,application/xhtml+xml,application/xml;\
			q=0.9,imgwebp,*/*;q=0.8"}

dirname = os.path.dirname(os.path.realpath('__file__'))
#dirname = os.path.dirname(os.path.realpath(sys.executable))
Comics_Page = "http://wasabisyrup.com"

# chrome download setting
chrome_options = webdriver.ChromeOptions()
preferences = {"download.default_directory": dirname,
               "directory_upgrade": True,
               "safebrowsing.enabled": True }
chrome_options.add_experimental_option("prefs", preferences)

def Initializing():
	
	os.system('cls')
	print("   |      |         |      |       ||||||")
	print("  | |    | |       ||     | |      |    |     ")
	print(" ||  |  |  ||     ||  |  |  ||     |              ")
	print(" ||   ||   ||     ||   ||   ||     |    |     ")
	print(" ||   ||   ||     ||   ||   ||     ||||||   Ver. 0.1 by IML")

	print("\n$ HI! THIS IS MARUAMRU COLLECTOR! $\n")
	mode = input("[*] MODE is All or Single ?(a/s) ")
	return mode



def URLparser(URL):
	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.implicitly_wait(1)
	driver.get(URL)
	return driver



def MultiCollect(driver):
	bs0bj = BeautifulSoup(driver.page_source, "html.parser")
	Allcomics =bs0bj.findAll("a",{"href":re.compile("http://www.shencomics.com/archives/.*")})\
		     +bs0bj.findAll("a",{"href":re.compile("http://www.yuncomics.com/archives/.*")})\
		     +bs0bj.findAll("a",{"href":re.compile("http://wasabisyrup.com/archives/.*")})
	Comic_count = 1
	Comic_total = len(Allcomics)	     

	for url in Allcomics:
		drv = URLparser(url.attrs['href'])
		SingleCollect(drv,Comic_count,Comic_total)
		Comic_count += 1



def SingleCollect(driver,Comic_count,Comic_total):
	bs0bj = BeautifulSoup(driver.page_source, "html.parser")
	comic_title = Collecting(bs0bj,Comic_count,Comic_total)

	if comic_title == "Protected":
		print("[*] This comic is Protected! Fail!")
	else:
		filelist = makePDF(comic_title)
		Removing(filelist)



def Collecting(bs0bj,Comic_count,Comic_total):
	os.system('cls')
	print("< Current Progress >")
	print("Total: " + str(Comic_count) + " / " + str(Comic_total))

	protect = bs0bj.find("h2")
	if protect != None :
		return protect.get_text()

	comic_title = bs0bj.find("div",{"class":"article-title"}).attrs['title']
	title_filter = '\\/<>:?!*"|'
	comic_title = comic_title.translate({ ord(x): y for (x, y) in zip(title_filter, "          ") })

	comic_images = bs0bj.findAll("img")
	count = 1

	for img in comic_images:
		imgurl = Comics_Page + img.attrs['data-src']
		imgfile = dirname + "\\" + comic_title + "_(" + "%04d" % count + ").jpg"
		count = count + 1
		print("\n# Link: " + imgurl)
		print("||\n||\n# Downloading to ->  " + imgfile)
		download(imgurl,imgfile)

		os.system('cls')
		print("< Current Progress >")
		print("# Total: " + str(Comic_count) + " / " + str(Comic_total))
		print("# Collecting " + comic_title + "\n# Progress:[", end='')
		for i in range(13):
			if (i / 13) <= (count / len(comic_images)):
				print("ㅁ", end ='')
			else:
				print("   ", end='')
		print(' ]')

	return comic_title

'''
def download(url , file_name):
	driver = webdriver.Chrome(chrome_options=chrome_options)
	time.sleep(3)
	response = driver.get(url)
	print(response)
	time.sleep(1)
	with open(file_name, "wb") as file:
		file.write(response)
'''
def download(url, file_name):
	session = requests.Session()
	req = session.get(url, headers = header)

	with open(file_name, "wb") as file:
		file.write(req.content)



def makePDF(comic_title):
	try:
		with open(comic_title + ".pdf", "wb") as f:
			f.write(img2pdf.convert([i for i in os.listdir(dirname) if i.endswith(".jpg")]))
		print("[*] Combing to PDF file.")
	except:
		print("[*] PDF File Can't Make.")
		print("[*] Program Down!")
		sys.exit(1)

	return os.listdir(dirname)


def Removing(filelist):
	for file in filelist:
		path = os.path.join(dirname, file)
		if path.endswith(".jpg"):
			os.remove(path)
	print("[*] Removing image files.")



if __name__ == '__main__':

	mode = Initializing()

	if mode != 'a' and mode != 's':
		print("[*] plz right command.")
		sys.exit(1)

	URL = input("[*] Please input URL(only MARUMARU): ")
	driver= URLparser(URL)
	print("[*] URL Parsing & Web Crawling...")

	if mode == 's':
		SingleCollect(driver,1,1)
	else:
		MultiCollect(driver)

	print("[*] Complete!")
