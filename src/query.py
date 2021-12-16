import requests
from bs4 import BeautifulSoup
import re

base_url = "https://gogoanime.wiki/"

GREEN = '\033[92m'
ERROR = '\033[93m'
END = '\x1b[0m'

def pages(url):
    
    pages = []
    
    querys = requests.get(url)
    soup = BeautifulSoup(querys.content, "html.parser")
    for link in soup.find_all('a', attrs={'data-page': re.compile("^ *\d[\d ]*$")}):
        pages.append(link.get('data-page'))
    
    try:
        return int(pages[-1])
    except:
        return 1
    
def query(search_input):
    
    #extract links from search url
    links = []
    search_url = base_url + "/search.html?keyword=" + search_input
    
    for i in range(pages(search_url)):
        querys = requests.get(search_url + "&page=" + str(i + 1))
        soup = BeautifulSoup(querys.content, "html.parser")

        for link in soup.find_all('a', attrs={'href': re.compile("^/category")}):
            links.append(link.get('href'))
    
    
    if not links:
        print(ERROR + "No search results found")
        quit()
    
    #delete double entrys and append to previous list
    
    temp_list = []
    for i in links:
        if i not in temp_list:
            temp_list.append(i)
        else:
            pass  
    
       
    links.clear()
    links.extend(temp_list)
    temp_list.clear()
    
    list_index = 1
    for j in links:
        print(GREEN + "["+  str(list_index) + "]" +  END + " " + str(j.replace("/category/", "")))  
        list_index += 1
        
   
    
    #get the right anime

    which_anime = input("Enter Number: ")
    
    try: 
        link = links[int(which_anime) - 1]
    except:
        print(ERROR + "Invalid Input")
        quit()
    
    link = base_url + link.replace("/", "", 1)
       
    
    return link


def episode(url):
    
    ep_count = []
    querys = requests.get(url)
    soup = BeautifulSoup(querys.content, "html.parser")
    for link in soup.find_all('a', attrs={'ep_end': re.compile("^ *\d[\d ]*$")}):
        ep_count.append(link.get('ep_end'))
    
    while True:
        which_episode = input("Episode " + GREEN + "[1-" + ep_count[-1] + "]" + END + ": ")
        try:
            if int(which_episode) in list(range(1, int(ep_count[-1]) + 1)):
                break
            else:
                print(ERROR + "Number out of range.")
                
        except:
            print(ERROR + "Invalid Input")
            
            
    video_url = url.replace("/category", "") + "-episode-" + which_episode

    return video_url