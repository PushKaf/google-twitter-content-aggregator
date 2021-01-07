from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import whitelistUtil as wu


#adds a "+" in if the string has spaces.
def parse(string):	
		strt = string.replace(" ", "+")
		return strt

#Main function that uses a whitelist to return search results
def whitelistGoogleSearch(pQueryRaw, pChc):
	base = "https://www.google.com/"
	
	#final string, is concatenated and returned, with html tags to show in the wepage
	restm = " "
	
	#whitelist based on what source the user wants to see from
	whitelist = wu.readGoogleWhitelist()
	#User given query, it is raw currently, because it needs to add "+" in between spaces, and add whitelist domain names at the end
	queryRaw = pQueryRaw
	counter= 0 
	chc = pChc
	for i in whitelist:

		#Whole point is to seperate the "www." and  ".com" from the items in the list
		if i[0:4] == "www.":
			parsedWhitelist = (i.split("www.")[1])
		else:
			parsedWhitelist = i
		#This is because some sites, the user wants to whitelist might not all have ".com", ie. ".net"
		try:
			parsedWhitelist = parsedWhitelist.split(".com")[0]
		except Exception as e:
			print("Not a dot com")
			print(e)
			break

		#Actual query thats gotten. Adds "+" if the rawQuery had spaces and adds domainName of the the items in the whitelist
		query = parse(queryRaw) + "+" + parsedWhitelist
		
		#Require different links for all params, such as, "past hour", and "24 hour"
		if chc.lower() == "past hour":
			link = f"https://www.google.com/search?q={query}&hl=en&tbs=qdr:h,sbd:1&tbm=nws&sxsrf=ALeKk007qEFyuVIwtayWo0LKk6ulCEfVFA:1602034996085&source=lnt&sa=X&ved=0ahUKEwirx--2raHsAhXyguAKHbWOAYYQpwUIJg&biw=1920&bih=937&dpr=1"
		elif chc.lower() == "24 hour":
			link = f"https://www.google.com/search?q={query}&rlz=1C1CHBF_enUS916US916&tbs=sbd:1,qdr:d&tbm=nws&sxsrf=ALeKk03iObI3skTb1cIAtZSfScYxTvIpSg:1602034537188&source=lnt&sa=X&ved=0ahUKEwifzYbcq6HsAhURZN8KHSZwCXsQpwUIJg&biw=1920&bih=937&dpr=1"
		elif chc.lower() == "google":
			link = f"https://www.google.com/search?q={query}&tbas=0&sxsrf=ALeKk038OhKLR7giou2CLYiJcEAELEpqhQ:1602038770171&source=lnt&tbs=qdr:d&sa=X&ved=2ahUKEwjwxb--u6HsAhXkdM0KHTjSBqQQpwV6BAgnEBw&biw=1920&bih=937"
		
		req = Request(link, headers={"User-Agent": "Mozilla/5.0"})
		wepage = urlopen(req).read()
		with requests.Session() as c:
			soup = BeautifulSoup(wepage, "html5lib")
			for item in soup.find_all("div", attrs={"class": "ZINbbc xpd O9g5cc uUPGi"}):
					try:
						#Gets the raw links, however once clicked, it will give a page not found error; need to parse
						rawLinks = (item.find('a', href=True)['href'])

						#Makes the link acctually right
						links = (rawLinks.split("/url?q=")[1]).split("&sa=U&")[0]
						print(links)						
						#Finds the title in the google item
						try:
							title = item.find('div', attrs={"class": "BNeawe vvjwJb AP7Wnd"}).get_text()
						except Exception as e:
							print("title error")
							print(e)

						#gets the description of the google item, with the following classes (All the items have same classes, which is why this works)
						description = item.find('div', attrs={"class": "BNeawe s3v9rd AP7Wnd"}).get_text()
						
						#seperates "https://" to get just the domain name
						try:
							domainName = ((links.split("https://")[1].split("/")[0]))
						except Exception as e:
							print("Domain Name Error")
							print(e)

						#checks the domain name of all the news sources gathered, if new sources do not have mathing name for our whitelist, they dont get added to the final output.
						if domainName in whitelist:
							#Sometimes, enountered unicode errors... 
							try:
								restm +=  f"<strong><u>{domainName}</u></strong>" + "</br>" + f"{title}" + "</br>" + description + "</br>" + f"<a href={links}>Link</a>" + "</br></br>"
							except Exception as e:
								print(e)		
						else:
							print("No News")
							pass
							
					except Exception as e:
						print(e)
	return restm

#Same function as google, however, the whitelist is taken off, it displays all results, from all sources.
def noWhiteListGoogleSearch(pQueryRaw, pChc):
	base = "https://www.google.com/"
	restm = " "
	counter= 0 
	chc = pChc
	query = parse(pQueryRaw)
	
	if chc.lower() == "past hour":
		link = f"https://www.google.com/search?q={query}&hl=en&tbs=qdr:h,sbd:1&tbm=nws&sxsrf=ALeKk007qEFyuVIwtayWo0LKk6ulCEfVFA:1602034996085&source=lnt&sa=X&ved=0ahUKEwirx--2raHsAhXyguAKHbWOAYYQpwUIJg&biw=1920&bih=937&dpr=1"
	elif chc.lower() == "24 hour":
		link = f"https://www.google.com/search?q={query}&rlz=1C1CHBF_enUS916US916&tbs=sbd:1,qdr:d&tbm=nws&sxsrf=ALeKk03iObI3skTb1cIAtZSfScYxTvIpSg:1602034537188&source=lnt&sa=X&ved=0ahUKEwifzYbcq6HsAhURZN8KHSZwCXsQpwUIJg&biw=1920&bih=937&dpr=1"
	elif chc.lower() == "google":
		link = f"https://www.google.com/search?q={query}&tbas=0&sxsrf=ALeKk038OhKLR7giou2CLYiJcEAELEpqhQ:1602038770171&source=lnt&tbs=qdr:d&sa=X&ved=2ahUKEwjwxb--u6HsAhXkdM0KHTjSBqQQpwV6BAgnEBw&biw=1920&bih=937"
	
	req = Request(link, headers={"User-Agent": "Mozilla/5.0"})
	wepage = urlopen(req).read()
	with requests.Session() as c:
		soup = BeautifulSoup(wepage, "html5lib")
		for item in soup.find_all("div", attrs={"class": "ZINbbc xpd O9g5cc uUPGi"}):
				try:
					rawLinks = (item.find('a', href=True)['href'])
					try:
						links = (rawLinks.split("/url?q=")[1]).split("&sa=U&")[0]
					except:
						pass

					try:
						title = item.find('div', attrs={"class": "BNeawe vvjwJb AP7Wnd"}).get_text()
					except Exception as e:
						print("title error")
						print(e)
					
					description = item.find('div', attrs={"class": "BNeawe s3v9rd AP7Wnd"}).get_text()

					try:
						domainName = ((links.split("https://")[1].split("/")[0]))
					except Exception as e:
						print("Domain Name Error")
						print(e)

					try:
						restm +=  f"<strong><u>{domainName}</u></strong>" + "</br>" + f"{title}" + "</br>" + description + "</br>" + f"<a href={links}>Link</a>" + "</br></br>"
					except Exception as e:
						#restm +=  "</br>" + f"{title}" + "</br>" + description + "</br>" + f"<a href={links}>Link</a>" + "</br></br>"
						print(e)
				except:
					return None	

	return restm

def google(pWhitelistChoice, pQuery, pTimeChoice):
	if pWhitelistChoice == "Whitelist":
		data = whitelistGoogleSearch(pQuery, pTimeChoice)
		return data
	else:
		data = noWhiteListGoogleSearch(pQuery, pTimeChoice)
		return data
