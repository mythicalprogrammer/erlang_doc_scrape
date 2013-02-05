from bs4 import BeautifulSoup

lists = open("lib/stdlib-1.19/doc/html/lists.html", "r")
soup = BeautifulSoup(lists)
#soup = BeautifulSoup(soup.prettify().encode('UTF-8'))

#print soup.prettify().encode('UTF-8')

soup = soup.find("div",{"id":'content'}).find("div",{"class":"innertube"})


#soup = BeautifulSoup(soup.prettify().encode('UTF-8'))


info = soup.find_all('div',{"class":"REFBODY"})
module = info[0].text.strip()
summary = info[1].text.strip()
description = info[2]
description = BeautifulSoup(description.prettify()).html.body.div.contents
description = [x.encode('UTF-8') for x in description if x != '\n' ]
description = [x for x in description if x != '' ]
description = ''.join(map(str, description))
#print description

#print len(soup.contents)
#print soup.contents[4].name
for i in range(0, len(soup.contents)):
	if hasattr(soup.contents[i], 'name') and soup.contents[i].name == 'p':
		if i > 24:
			print i
			#print soup.contents[i].prettify()
			function = soup.contents[i].find('a')['name']
			print "function:"
			print function
			semantic = soup.contents[i].find('span').text.strip()
			#print "semantic:"
			#print semantic
			types = soup.contents[i].div.contents
			types = soup.contents[i].div.p.replaceWith('')
			types = soup.contents[i].div.contents
			types = [x.encode('UTF-8') for x in types if x != '\n' ]
			types = [x for x in types if x != '' ]
			types = ''.join(map(str, types))
			types = BeautifulSoup(types).prettify()
			print "types:"
			print types
			summary = soup.contents[i+2].findChildren()[0].findChildren()[0]
			print "summary:"
			print summary

	if i > 26:
		break
#i = 0
#for content in soup.contents:
	#print i
#	i += 1
#	if content != '':
#		print ''
		#print soup.contents[i]
#		print soup.contents[i].name
#	if i > 3:
#		break
#print(soup.contents[0])
#print(soup.contents[3])
#tag name
#print soup.contents[4].name

