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
    if i > 0:
        break
    href = li_list[i].a["href"]
    href = dir[:-10] + href 
    soup = soupify(href)
    soup = soup.find("div",{"id":'content'}).find("div",{"class":"innertube"})
    info = soup.find_all('div',{"class":"REFBODY"})
    module = info[0].text.strip()
    summary = info[1].text.strip()
    description = info[2].contents
    description = [re.sub('\n','',x.encode('UTF-8')) for x in description if x != '\n' ]
    description = [ re.sub(' +',' ',x) for x in description ]
    description = ''.join(map(str, description))
    description = description[7:]
    sql_module+= "INSERT INTO modules (app_id,name,summary,description) "
    sql_module+= "VALUES (5,'"+module+"','"+summary+"','"+description+"');"
    sql_module+= "\n"; 
    sql_module+= "\n"; 

#print sql_module
#print module
#print summary
#print description
    #sql_module+= "INSERT INTO modules (app_id,name,summary,description) "
    #sql_module+= 'VALUES ("5","'+module+'","'summary'","'+description+'");' 
#f = open('sql_apps.sql', 'w')
#f.write(sql_apps)
#f.close()
#print soup.contents[18]
#print soup.contents[34].name
#function = soup.contents[34].find('a')['name']
#print function 
all_function_in_module = []
FLAG_FUNCTION_SECTION = False
for i in range(0, len(soup.contents)):
    FLAG_FUNCTION_SEE_MORE = False
    list_func = [] # function name, syntax, types, summary
    if (
            FLAG_FUNCTION_SECTION and
            hasattr(soup.contents[i], 'name') and 
            soup.contents[i].name == 'p' 
       ):
        fun_list = soup.contents[i].findAll("a",{"name":True})
        fun_list_name = []
        for j in range(0, len(fun_list)):
            fun_list_name.append(str(fun_list[j]["name"]))
        syntax_list = soup.contents[i].findAll("span",{"class":"bold_code"})
        syntax_list = [re.sub(r'[\xc2\xa0]'," ",re.sub('<[^<]+?>', '',re.sub('<br/>','\n',x.renderContents()))) for x in syntax_list]
        fun_name_syntax_list = zip(fun_list_name, syntax_list)
        #print fun_name_syntax_list
        #fun_name_syntax_list = zip(fun_list_name, syntax_list)
        types = ''
        if (
            hasattr(soup.contents[i+1], 'p') and
            soup.contents[i+1].p.text == "Types:"
          ):
          types = soup.contents[i+1].div
          types = [x.encode('UTF-8') for x in types if x != '\n' ]
          types = [x for x in types if x != '' ]
          types = [re.sub('<[^<]+?>', '',re.sub('<br/>','\n',x)) for x in types]
          types = ''.join(map(str, types))
          types = re.sub(' +',' ',types)
          types = re.sub('\n',' ',types)
          fun_info = soup.contents[i+3].findAll("p")
        else:
          fun_info = soup.contents[i+2].findAll("p")
        if len(fun_info) == 3 and hasattr(fun_info[2], 'strong'):
            if hasattr(fun_info[2].strong, 'content'):
                if fun_info[2].strong.contents == "See also:":
                    see_more = fun_info[2].span.a.text.strip()
                    FLAG_FUNCTION_SEE_MORE = True 
        function_summary = ''
        if FLAG_FUNCTION_SEE_MORE: 
            function_summary = fun_info[1].contents
            function_summary = [x.encode('UTF-8') for x in function_summary if x != '\n' ]
            function_summary = [x for x in function_summary if x != '' ]
            function_summary = ''.join(map(str, function_summary))
            function_summary = re.sub(' +',' ',function_summary)
            function_summary = re.sub('\n',' ',function_summary)
            #function_summary = re.sub('<[^<]+?>', '',function_summary)
            function_summary = re.sub(r'[\xc2\xa0]'," ",function_summary)
            function_summary = re.sub('<[^<]+?>', '',function_summary)
        else:
            for l in range(1,len(fun_info)):
                function_summary_temp = fun_info[l].contents
                function_summary_temp = ''.join(map(str, function_summary_temp))
                function_summary += str(function_summary_temp)
                function_summary = [x.encode('UTF-8') for x in function_summary if x != '\n' ]
                function_summary = [x for x in function_summary if x != '' ]
                function_summary = ''.join(map(str, function_summary))
                function_summary = re.sub(' +',' ',function_summary)
                function_summary = re.sub('<[^<]+?>', '',function_summary)
                function_summary = re.sub(r'[\xc2\xa0]'," ",function_summary)
        for k in range(0,len(fun_name_syntax_list)):
            fun_name_syntax_list[k] = tuple(list(fun_name_syntax_list[k]) + [function_summary])
            """
            if len(types) > 0:
                fun_name_syntax_list[k] = tuple(list(fun_name_syntax_list[k]) + [types] + [function_summary])
            else:
                fun_name_syntax_list[k] = tuple(list(fun_name_syntax_list[k]) + [function_summary])
            """
        """
        dic_temp = {}
        for k in range(0,len(fun_name_syntax_list)):
            dic_temp["name"] = fun_name_syntax_list[k][0] # name
            dic_temp["syntax"] = fun_name_syntax_list[k][1] # syntax 
            dic_temp["summary"] = fun_name_syntax_list[k][2] # summary 
            all_function_in_module += [dic_temp]
        """
        all_function_in_module += fun_name_syntax_list 
        #print dic_temp
        print all_function_in_module
        #print fun_name_syntax_list[0][2]
        #print len(fun_name_syntax_list)
        #print fun_name_syntax_list
    if (
            hasattr(soup.contents[i], 'name') and 
            soup.contents[i].name == 'h3' and
            soup.contents[i].text.strip() == 'EXPORTS' 
       ):
        FLAG_FUNCTION_SECTION = True

sql_function_array = ''            
for i in range(0, len(all_function_in_module)):
    name = all_function_in_module[i][0] # name
    syntax = all_function_in_module[i][1] # syntax 
    summary = all_function_in_module[i][2] # summary
    sql_function_array += "INSERT INTO funs (module_id,name,semantic,summary) "
    sql_function_array += 'VALUES ("1","'+name+'","'+syntax+'","'+summary+'");' 
    sql_function_array += '\n' 
    sql_function_array += '\n' 

#print sql_function_array
    #print all_function_in_module[i]
    #    print all_function_in_module
#sql_module+= "INSERT INTO modules (app_id,name,summary,description) "
#sql_module+= 'VALUES ("5","'+module+'","'summary'","'+description+'");' 
f = open('sql_function_array.sql', 'w')
f.write(sql_function_array)
f.close()
