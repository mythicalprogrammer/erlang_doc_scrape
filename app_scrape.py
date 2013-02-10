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
        #if td_list[0].table != None:
            #print app_soup[i].td.table.tr.td.find_all('a')
            #a_list = app_soup[i].td.table.tr.td.find_all('a')
            #print a_list[0].text # App Name
            #print a_list[1].text # App Version
    #if i > 1:
    #    break;

sql_apps = ''
for i in range(0, len(app_list)):
    sql_apps += "INSERT INTO apps (name,version,summary) "
    sql_apps += 'VALUES ("'+app_list[i][0]+'","'+app_list[i][1]+'","'+app_list[i][2]+'");' 
    sql_apps += "\n"
    sql_apps += "\n"

f = open('sql_apps.sql', 'w')
f.write(sql_apps)
f.close()
