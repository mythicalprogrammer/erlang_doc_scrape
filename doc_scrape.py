from bs4 import BeautifulSoup
import os

#app_list
#app_list = os.listdir('otp_doc_html_R16A_RELEASE_CANDIDATE/lib')
#app_list = [x.split('-')[0] for x in app_list]

app_html = open('otp_doc_html_R16A_RELEASE_CANDIDATE/doc/applications.html','r')
app_soup = BeautifulSoup(app_html).find_all('tr')
app_category = ''
app_list = []
sql_app_id_iter = 0
sql_app_id_lookup = {}
for i in range(0, len(app_soup)):
    if len(app_soup[i].attrs) == 0:
        if len(app_soup[i].td.attrs) == 2:
            app_category = app_soup[i].td.font.b.text.strip().encode('UTF-8') # App Category
   #         print app_soup[i].td.font.b.text # App Category
    elif len(app_soup[i].attrs) == 1:
        td_list = app_soup[i].find_all('td')
        if len(td_list) == 3:
           #print app_cat
           a_list = td_list[1].find_all('a')
           #print a_list[0].text # App Name
           #print a_list[1].text # App Version
           #print td_list[2].text.strip() # App Summary
           app_name = a_list[0].text.strip().encode('UTF-8') # App Name
           app_version = a_list[1].text.strip().encode('UTF-8') # App Version
           app_summary = td_list[2].text.strip().encode('UTF-8') # App Summary
	   app_list.append((app_name,app_version,app_summary,app_category))
	   sql_app_id_iter += 1 
	   sql_app_id_lookup[app_name] = sql_app_id_iter
        #if td_list[0].table != None:
            #print app_soup[i].td.table.tr.td.find_all('a')
            #a_list = app_soup[i].td.table.tr.td.find_all('a')
            #print a_list[0].text # App Name
            #print a_list[1].text # App Version
    #if i > 1:
    #    break;

#print app_list
#print len(app_list) # 54
#print sql_app_id_lookup
#print sql_app_id_lookup['Basic'] # 1
#print sql_app_id_lookup['Miscellaneous'] # 9
#print len(sql_app_id_lookup) # 54 

"""
#print app_soup[1]
#for i in range(0, len(app_soup)):
#    print app_soup[i]
#    if i > 2:
#        break;

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
"""
