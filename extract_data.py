import requests
from bs4 import BeautifulSoup
from pathlib import Path
import os
import tqdm 

class HTMLScapper():
    def __init__(self,main_web_url:str,web_data_dir:str):
        """
        This class intends to scrap and save all HTML pages from a given website. 

        Args:
            main_web_url (str): The main URL of the website to scrap
            web_data_dir (str): The directory where to save the HTML pages
        """
        self.main_url=main_web_url
        self.dicnry_links={} 
        self.dicnry_links[self.main_url]=0
        self.counter=0
        
        # Create a folder to save our HTML pages. 
        dest_f=self.main_url.split("://")[-1] # remove https:// or http://
        self.web_data_dir=os.path.join(web_data_dir,dest_f.replace(".","_"))
        if not os.path.isdir(self.web_data_dir):
            os.makedirs(self.web_data_dir,exist_ok=False)
        
        
    def get_all_links_this_page(self,url:str):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all("a", href=True):
            if str(link["href"]).startswith("/"):
                link_full=self.main_url+link["href"]
                if link_full not in self.dicnry_links:
                    print(f'New link discovered: {link_full}')
                    self.dicnry_links[link_full]=0
            
    def launch(self):
        while True:
            try:
                # get all un-visited web pages
                un_visited_urls=[]
                for url,item in self.dicnry_links.items():
                    if item==0:
                        un_visited_urls.append(url)
                for url in un_visited_urls:
                    self.get_all_links_this_page(url)
                    self.dicnry_links[url]=1
                    self.counter+=1
                    print("Completed for link:",url)
                    print("Completed",self.counter,"out of",len(list(self.dicnry_links.values())))
                if all(list(self.dicnry_links.values())):
                    break
    
            except requests.exceptions.HTTPError as errh:
                print ("Http Error:",errh)
                self.dicnry_links[url]=1
                pass
            except requests.exceptions.ConnectionError as errc:
                print ("Error Connecting:",errc)
                self.dicnry_links[url]=1
                pass
            except requests.exceptions.Timeout as errt:
                print ("Timeout Error:",errt)
                self.dicnry_links[url]=1
                pass
            except requests.exceptions.RequestException as err:
                print ("OOps: Something Else",err)
                self.dicnry_links[url]=1
                pass
            

    def save_retrieved_html(self):
        for url in tqdm.tqdm(self.dicnry_links.keys()):
            try:
                response = requests.get(url)
                file_name=url+".html"
                file_name=file_name.replace("/","_")
                file_path = os.path.join(self.web_data_dir, file_name)
                with open(file_path,"w") as f:
                    f.write(response.text)
            except:
                print(f'Issue on url: {url}')
                pass
   
if __name__ =='__main__':
         scrapper = HTMLScapper(main_web_url='https://go.sellsy.com',web_data_dir = 'web_data')
         scrapper.launch()
         scrapper.save_retrieved_html()
         
       
