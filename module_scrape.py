from bs4 import BeautifulSoup
import os
import re 
import cgi

root_dir = 'otp_doc_html_R16A_RELEASE_CANDIDATE/'
#app_list
#app_list = os.listdir('otp_doc_html_R16A_RELEASE_CANDIDATE/lib')
#app_list = [x.split('-')[0] for x in app_list]

app_html = open('otp_doc_html_R16A_RELEASE_CANDIDATE/doc/applications.html','r')
app_soup = BeautifulSoup(app_html).find_all('tr')
app_category = ''
app_list = []
sql_app_id_iter = 0
sql_app_id_lookup = {}
app_link_lookup = {}
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
            app_link = root_dir + a_list[0]['href'].strip().encode('UTF-8')[3:] # App URL 
            app_name = a_list[0].text.strip().encode('UTF-8') # App Name
            app_version = a_list[1].text.strip().encode('UTF-8') # App Version
            app_summary = td_list[2].text.strip().encode('UTF-8') # App Summary
            app_summary = [x.encode('UTF-8') for x in app_summary if x != '\n' ]
            app_summary = ''.join(map(str, app_summary))
            app_summary = re.sub(' +',' ', app_summary)
        app_list.append((app_name,app_version,app_summary,app_category))
        sql_app_id_iter += 1 
        sql_app_id_lookup[app_name] = sql_app_id_iter
        app_link_lookup[app_name] = app_link 


#print app_list[0]
#('erts', '5.10', 'Functionality necessary to run the Erlang System itself', 'Basic')
#name version summary category
#INSERT INTO table_name (name,version,summary,category)
#VALUES (value1, value2, value3,...)
#print len(app_list) # 54
#print sql_app_id_lookup
#print sql_app_id_lookup['Basic'] # 1
#print sql_app_id_lookup['Miscellaneous'] # 9
#print len(sql_app_id_lookup) # 54 
#print app_link_lookup
#print len(app_link_lookup) # 54

"""
Going Through Each App and Scraping.
"""
"""
dir = app_link_lookup["sasl"]
app_html = open(dir,'r')
app_soup = BeautifulSoup(app_html).find('ul', {'class':'flipMenu'})
print app_soup.prettify()
"""

"""
craping stdlib
"""
app_id = sql_app_id_lookup['stdlib'] # 5
dir = app_link_lookup["stdlib"]
app_html = open(dir,'r')
flip_soup = BeautifulSoup(app_html).find('ul', {'class':'flipMenu'})



#####
#app html
#####
first_li = flip_soup.find('li')
#print first_li.a.text.encode('UTF-8').strip()
href = first_li.a["href"]
app_href = dir[:-10] + href 
#print app_href
app_info_page = open(app_href,'r')
app_info_soup = BeautifulSoup(app_info_page).find('div', {'id':'content'}).div
#print app_info_soup
info = app_info_soup.find_all('div',{"class":"REFBODY"})
module = info[0].text.strip()
summary = info[1].text.strip()
#print info[2].findAll("p")[1].text
#description = info[2].p.p.text
description = info[2].findAll("p")[1].text
description = [x.encode('UTF-8') for x in description if x != '\n' ]
description = [x for x in description if x != '' ]
description = ''.join(map(str, description))
description = re.sub(' +',' ',description)
configuration = info[3]
see_also = info[4].p.text
see_also = [x.encode('UTF-8') for x in see_also if x != '\n' ]
see_also = ''.join(map(str, see_also))
see_also = re.sub(' +',' ', see_also)
#print 'app: '+module
#print 'app_summary: '+summary
#print 'app_description: '+description
#print 'app_see_also: '+see_also

"""
Going through the table of contents lists with folders icon
"""
def soupify(url):
    html_file = open(url,'r')
    return BeautifulSoup(html_file)

li_list = flip_soup.findAll('li',{'id':'no'})
sql_module = ''
for i in range(0, len(li_list)):
    if i > 8:
        break
    href = li_list[i].a["href"]
    href = dir[:-10] + href 
    soup = soupify(href)
    soup = soup.find("div",{"id":'content'}).find("div",{"class":"innertube"})
    info = soup.find_all('div',{"class":"REFBODY"})
    module = info[0].text.strip().encode('UTF-8')
    summary = info[1].text.strip().encode('UTF-8')
    description = info[2].contents
    description = [re.sub('\n','',x.encode('UTF-8')) for x in description if x != '\n' ]
    description = [ re.sub(' +',' ',x) for x in description ]
    description = [ re.sub('%','\%',x) for x in description ]
    description = [ re.sub("'","\\'",x) for x in description ]
    description = ''.join(map(str, description))
    description = description[7:]
    sql_module+= "INSERT INTO modules (app_id,name,summary,description) "
    sql_module+= "VALUES (5,'"+module+"','"+summary+"','"+description+"');"
    sql_module+= "\n"; 
    sql_module+= "\n"; 

#print module
#print summary
#print description
#print sql_module
f = open('sql_module_stdlib.sql', 'w')
f.write(sql_module)
f.close()
