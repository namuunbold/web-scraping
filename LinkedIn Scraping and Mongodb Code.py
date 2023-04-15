#!/usr/bin/env python
# coding: utf-8

# In[4]:


from bs4 import BeautifulSoup
import requests
import time
import re
import requests
import os
from urllib.request import urlopen
import requests
import pymongo
import ast
import http.client, urllib.parse
import json

job_titles = ["business analyst","data scientist","business intelligence","market analyst"]


# In[2]:


'''
start = 0
keywords = "business%20analyst"
location = "United%20States"
soup_objects = []
for i in range(0,4):
    URL ="https://www.linkedin.com/jobs/search/?currentJobId=3519711014&geoId=103644278&keywords="+keywords+"&location="+location+"&refresh=true&start="+str(start)
    print(URL)
    #conducting a request of the stated URL above:
    page = requests.get(URL)
    print(page)
    soup = BeautifulSoup(page.text, "html.parser")
    soup_objects.append(soup)
    start = start + 25
    time.sleep(15)
'''


# In[5]:


## Creating soup objects for the top 4 pages
def get_soup_objects(urls):
    soup_objects = []
    for URL in urls:

        print(URL)
        #conducting a request of the stated URL above:
        page = requests.get(URL)
        print(page)
        soup = BeautifulSoup(page.text, "html.parser")
        soup_objects.append(soup)
        time.sleep(25)
    return soup_objects


# In[6]:


## Collecting 100 job urls for business analyst
def get_job_urls(soup_objects):
    job_urls = []

    for soup in soup_objects:
        urls = []
        for h in soup.findAll('li'):    
            a = h.find('a')
            try:        
                if 'href' in a.attrs:            
                    url = a.get('href')
                    urls.append(url)
            except:
                pass

        # Only taking the job urls on each page
        job_urls.append(urls[0:25])
        i =0
        for url in urls[0:25]:
            print(i+1)
            print(url)
            i=i+1
    return job_urls


# In[5]:


'''import pandas as pd
data = pd.DataFrame(job_urls) 
data.to_excel("/Users/sahit/OneDrive/Desktop/LinkedIn_urls.xlsx")'''


# In[7]:


## Converting to flat list and removing duplicate urls from the list
def get_flat_list(job_urls):
    job_urls = [url for sublist in job_urls for url in sublist]
    x = job_urls
    x = list(set(x))
    len(x)
    return x


# In[8]:


## Saving each job url as a htm file
def download_htm(x,path):
    i = 0
    for url in x:
        page = requests.get(url)
        i=i+1
        print(i,": ",page,"job_"+str(i)+".htm")
        print(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        #file = open("/Users/sahit/OneDrive/Desktop/DDR Final Project" + path + "job_"+str(i)+".htm", 'w',encoding="utf-8")
        file = open(path + "job_"+str(i)+".htm", 'w',encoding="utf-8")
        for page in soup.find_all():
            content = page.prettify()
            file.write(content)
        file.close()
        time.sleep(15)


# In[2]:


def extract_job_attributes(path,key,urls):
    all_jobs = []
    for i in range(1,301):
        info_dict = {}
        #file = open("/Users/sahit/OneDrive/Desktop/DDR Final Project"+ path + "job_"+str(i)+".htm",'r',encoding="utf-8")
        file = open(path + "job_"+str(i)+".htm",'r',encoding="utf-8")
        data = file.read()
        file.close()
        soup = BeautifulSoup(data, "html.parser")
        print(i,":")

        ## Get job title
        job_title = soup.find_all('h1',class_="top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title")
        if job_title:
            job_title = (job_title[0].text).strip()
            print("job title: ",job_title)
        else:
            job_title = ""
        ## Company name
        company = soup.find("a",class_="topcard__org-name-link topcard__flavor--black-link")
        if company:
            company = company.text.strip()
            print("company: ", company)
        else:
            company = ""
        ## Location
        location = soup.find("span",class_="topcard__flavor topcard__flavor--bullet")
        if location:
            location = location.text.strip()
            print("location: ",location)
        else:
            location = ""
        ## Posted How Long AGO
        posted = soup.find("span",class_="posted-time-ago__text topcard__flavor--metadata")
        if posted:
            posted = posted.text.strip()
            print("posted: ",posted)
        else:
            posted = ''
            print("posted: ",posted)
        ## Number of Applicants
        applicants = soup.find("figcaption",class_="num-applicants__caption")
        if applicants:
            applicants = applicants.text.strip()
            print("number of applicants: ",applicants)
        else:
            applicants = ''
            print("applicants: ",applicants)
        ## Featured Benefits
        benefits = soup.find("ul",class_="featured-benefits__list")
        if benefits:
            ben = []
            for b in benefits: 
                if b:
                    b = b.text.strip()
                    #b = b.split()
                    #b = " ".join(b)
                    ben.append(b)
            ben = [i for i in ben if i]
            benefits = ben
            print("featured benefits: ",benefits)
        else:
            benefits = ''
            print("featured benefits: ",benefits)
        ## JOB Description
        jd = soup.find("div",class_="show-more-less-html__markup")
        if jd:
            jobd = []
            for b in jd: 
                if b:
                    b = b.text.strip()
                    jobd.append(b)
            jd = [i for i in jobd if i]
            jd = " ".join(jd)
            jd = jd.replace("\n", "")
            print("job description: ",jd)
        else:
            jd = ''
            print("job description: ",jd)
        ## Criteria List
        job_info = soup.find('ul',class_="description__job-criteria-list")
        if job_info:
            for info in job_info:
                info = info.text.strip()
                info = info.split()
                sl = ''
                et = ''
                jb = ''
                ind = ''
                if info:
                    ## Seniority Level
                    if "Seniority" in info:
                        sl = " ".join(info[2:])
                        print("seniority level: ",sl)
                        info_dict["Seniority Level"] = sl
                    ## Employment Type
                    if "Employment" in info:
                        et = " ".join(info[2:])
                        print("employment type: ",et)
                        info_dict["Employment Type"] = et
                    ## Job Function
                    if "function" in info:
                        jb = " ".join(info[2:])
                        print("job function: ",jb)
                        info_dict["Job Function"] = jb
                    ## Industries
                    if "Industries" in info:
                        ind = " ".join(info[1:])
                        print("industries: ",ind)
                        info_dict["Industries"] = ind
                else:
                    continue
        else:
            job_info = ""

        ## Saving all attribute information in a dictionary
        info_dict["Search Term"] = key
        info_dict["Job Title"] = job_title
        info_dict["URL"] = urls[i-1]
        info_dict["Company"] = company
        info_dict["Location"] = location
        info_dict["Country"] = "United States"
        info_dict["Posted"] = posted
        info_dict["Number of Applicants"] = applicants
        info_dict["Benefits"] = benefits
        info_dict["Job Description"] = jd
        info_dict["Seniority Level"] = sl
        info_dict["Employment Type"] = et
        info_dict["Job Function"] = jb
        info_dict["Industries"] = ind
        
        
        
        ## Final list of dictionaries
        all_jobs.append(info_dict)
    return all_jobs


# # Scraping Business Analyst Jobs

# In[74]:


urls = ["https://www.linkedin.com/jobs/search/?currentJobId=3519711014&geoId=103644278&keywords=business%20analyst&location=United%20States&refresh=true","https://www.linkedin.com/jobs/search/?currentJobId=3527682791&geoId=103644278&keywords=business%20analyst&location=United%20States&refresh=true&start=25","https://www.linkedin.com/jobs/search/?currentJobId=3520061488&geoId=103644278&keywords=business%20analyst&location=United%20States&refresh=true&start=50","https://www.linkedin.com/jobs/search/?currentJobId=3524120873&geoId=103644278&keywords=business%20analyst&location=United%20States&refresh=true&start=75","https://www.linkedin.com/jobs/search/?currentJobId=3534586924&geoId=103644278&keywords=business%20analyst&location=United%20States&refresh=true&start=100","https://www.linkedin.com/jobs/search/?currentJobId=3519840495&geoId=103644278&keywords=business%20analyst&location=United%20States&refresh=true&start=125","https://www.linkedin.com/jobs/search/?currentJobId=3518652765&geoId=103644278&keywords=business%20analyst&location=United%20States&refresh=true&start=150","https://www.linkedin.com/jobs/search/?currentJobId=3511711843&geoId=103644278&keywords=business%20analyst&location=United%20States&refresh=true&start=175","https://www.linkedin.com/jobs/search/?currentJobId=3522027341&geoId=103644278&keywords=business%20analyst&location=United%20States&refresh=true&start=200","https://www.linkedin.com/jobs/search/?currentJobId=3518210835&geoId=103644278&keywords=business%20analyst&location=United%20States&refresh=true&start=225","https://www.linkedin.com/jobs/search/?currentJobId=3501483224&geoId=103644278&keywords=business%20analyst&location=United%20States&refresh=true&start=250","https://www.linkedin.com/jobs/search/?currentJobId=3537939677&geoId=103644278&keywords=business%20analyst&location=United%20States&refresh=true&start=275"]
soup_objects = get_soup_objects(urls)
job_urls = get_job_urls(soup_objects)
ba_job_urls = get_flat_list(job_urls)
path = "LinkedIn_pages_ba/"
download_htm(ba_job_urls,path)
key = "Business Analyst"
ba_jobs = extract_job_attributes(path,key,ba_job_urls)


# In[68]:


ba_job_urls[1]


# In[70]:


ba_jobs


# # Scraping Data Scientist Jobs

# In[75]:


urls = ["https://www.linkedin.com/jobs/search/?currentJobId=3521967086&geoId=103644278&keywords=data%20scientist&location=United%20States&refresh=true","https://www.linkedin.com/jobs/search/?currentJobId=3526430960&geoId=103644278&keywords=data%20scientist&location=United%20States&refresh=true&start=25","https://www.linkedin.com/jobs/search/?currentJobId=3516616194&geoId=103644278&keywords=data%20scientist&location=United%20States&refresh=true&start=50","https://www.linkedin.com/jobs/search/?currentJobId=3529689215&geoId=103644278&keywords=data%20scientist&location=United%20States&refresh=true&start=75","https://www.linkedin.com/jobs/search/?currentJobId=3532818297&geoId=103644278&keywords=data%20scientist&location=United%20States&refresh=true&start=100","https://www.linkedin.com/jobs/search/?currentJobId=3522683748&geoId=103644278&keywords=data%20scientist&location=United%20States&refresh=true&start=125","https://www.linkedin.com/jobs/search/?currentJobId=3529458696&geoId=103644278&keywords=data%20scientist&location=United%20States&refresh=true&start=150","https://www.linkedin.com/jobs/search/?currentJobId=3534247485&geoId=103644278&keywords=data%20scientist&location=United%20States&refresh=true&start=175","https://www.linkedin.com/jobs/search/?currentJobId=3532872315&geoId=103644278&keywords=data%20scientist&location=United%20States&refresh=true&start=200","https://www.linkedin.com/jobs/search/?currentJobId=3530980479&geoId=103644278&keywords=data%20scientist&location=United%20States&refresh=true&start=225","https://www.linkedin.com/jobs/search/?currentJobId=3530954893&geoId=103644278&keywords=data%20scientist&location=United%20States&refresh=true&start=250","https://www.linkedin.com/jobs/search/?currentJobId=3531417369&geoId=103644278&keywords=data%20scientist&location=United%20States&refresh=true&start=275"]
soup_objects = get_soup_objects(urls)
job_urls = get_job_urls(soup_objects)
ds_job_urls = get_flat_list(job_urls)
path = "LinkedIn_pages_ds/"
download_htm(ds_job_urls,path)
key = "Data Scientist"
ds_jobs = extract_job_attributes(path,key,ds_job_urls)


# In[21]:


ds_job_urls[0:10]


# # Scraping Data Analyst Jobs

# In[ ]:


urls = ["https://www.linkedin.com/jobs/search/?currentJobId=3531350131&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true","https://www.linkedin.com/jobs/search/?currentJobId=3531215030&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start=25","https://www.linkedin.com/jobs/search/?currentJobId=3520070824&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start=50","https://www.linkedin.com/jobs/search/?currentJobId=3528173026&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start=75","https://www.linkedin.com/jobs/search/?currentJobId=3524219402&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start=100","https://www.linkedin.com/jobs/search/?currentJobId=3528173043&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start=125","https://www.linkedin.com/jobs/search/?currentJobId=3521949638&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start=150","https://www.linkedin.com/jobs/search/?currentJobId=3525758559&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start=175","https://www.linkedin.com/jobs/search/?currentJobId=3539109348&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start=200","https://www.linkedin.com/jobs/search/?currentJobId=3531328826&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start=225","https://www.linkedin.com/jobs/search/?currentJobId=3531420095&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start=250","https://www.linkedin.com/jobs/search/?currentJobId=3521163007&geoId=103644278&keywords=data%20analyst&location=United%20States&refresh=true&start=275"]
soup_objects = get_soup_objects(urls)
job_urls = get_job_urls(soup_objects)
da_job_urls = get_flat_list(job_urls)
path = "LinkedIn_pages_da/"
download_htm(da_job_urls,path)
key = "Data Analyst"
da_jobs = extract_job_attributes(path,key,da_job_urls)


# In[77]:


len(da_job_urls)


# # Scraping Business Intelligence Jobs

# In[23]:


urls = ["https://www.linkedin.com/jobs/search/?currentJobId=3498879485&geoId=103644278&keywords=business%20intelligence&location=United%20States&refresh=true","https://www.linkedin.com/jobs/search/?currentJobId=3530654117&geoId=103644278&keywords=business%20intelligence&location=United%20States&refresh=true&start=25","https://www.linkedin.com/jobs/search/?currentJobId=3523910415&geoId=103644278&keywords=business%20intelligence&location=United%20States&refresh=true&start=50","https://www.linkedin.com/jobs/search/?currentJobId=3526180208&geoId=103644278&keywords=business%20intelligence&location=United%20States&refresh=true&start=75","https://www.linkedin.com/jobs/search/?currentJobId=3527082211&geoId=103644278&keywords=business%20intelligence&location=United%20States&refresh=true&start=100","https://www.linkedin.com/jobs/search/?currentJobId=3517882645&geoId=103644278&keywords=business%20intelligence&location=United%20States&refresh=true&start=125","https://www.linkedin.com/jobs/search/?currentJobId=3539588107&geoId=103644278&keywords=business%20intelligence&location=United%20States&refresh=true&start=150","https://www.linkedin.com/jobs/search/?currentJobId=3539588106&geoId=103644278&keywords=business%20intelligence&location=United%20States&refresh=true&start=175","https://www.linkedin.com/jobs/search/?currentJobId=3539588108&geoId=103644278&keywords=business%20intelligence&location=United%20States&refresh=true&start=200","https://www.linkedin.com/jobs/search/?currentJobId=3539588104&geoId=103644278&keywords=business%20intelligence&location=United%20States&refresh=true&start=225","https://www.linkedin.com/jobs/search/?currentJobId=3521158166&geoId=103644278&keywords=business%20intelligence&location=United%20States&refresh=true&start=250","https://www.linkedin.com/jobs/search/?currentJobId=3504255181&geoId=103644278&keywords=business%20intelligence&location=United%20States&refresh=true&start=275"]
soup_objects = get_soup_objects(urls)
job_urls = get_job_urls(soup_objects)
bi_job_urls = get_flat_list(job_urls)
path = "LinkedIn_pages_bi/"
ownload_htm(bi_job_urls,path)
key = "Business Intelligence"
bi_jobs = extract_job_attributes(path,key,bi_job_urls)


# In[25]:


bi_job_urls[0:10]


# # Scraping Market Analyst Jobs

# In[62]:


urls = ["https://www.linkedin.com/jobs/search/?currentJobId=3488696886&geoId=103644278&keywords=market%20analyst&location=United%20States&refresh=true","https://www.linkedin.com/jobs/search/?currentJobId=3526084595&geoId=103644278&keywords=market%20analyst&location=United%20States&refresh=true&start=25","https://www.linkedin.com/jobs/search/?currentJobId=3497292820&geoId=103644278&keywords=market%20analyst&location=United%20States&refresh=true&start=50","https://www.linkedin.com/jobs/search/?currentJobId=3521949638&geoId=103644278&keywords=market%20analyst&location=United%20States&refresh=true&start=75","https://www.linkedin.com/jobs/search/?currentJobId=3519840495&geoId=103644278&keywords=market%20analyst&location=United%20States&refresh=true&start=100","https://www.linkedin.com/jobs/search/?currentJobId=3483770041&geoId=103644278&keywords=market%20analyst&location=United%20States&refresh=true&start=125","https://www.linkedin.com/jobs/search/?currentJobId=3420954066&geoId=103644278&keywords=market%20analyst&location=United%20States&refresh=true&start=150","https://www.linkedin.com/jobs/search/?currentJobId=3522027341&geoId=103644278&keywords=market%20analyst&location=United%20States&refresh=true&start=175","https://www.linkedin.com/jobs/search/?currentJobId=3517488843&geoId=103644278&keywords=market%20analyst&location=United%20States&refresh=true&start=200","https://www.linkedin.com/jobs/search/?currentJobId=3518057221&geoId=103644278&keywords=market%20analyst&location=United%20States&refresh=true&start=225","https://www.linkedin.com/jobs/search/?currentJobId=3501800087&geoId=103644278&keywords=market%20analyst&location=United%20States&refresh=true&start=250","https://www.linkedin.com/jobs/search/?currentJobId=3428145389&geoId=103644278&keywords=market%20analyst&location=United%20States&refresh=true&start=275"]
soup_objects = get_soup_objects(urls)
job_urls = get_job_urls(soup_objects)
ma_job_urls = get_flat_list(job_urls)
path = "LinkedIn_pages_ma/"
download_htm(ma_job_urls,path)
key = "Market Analyst"
ma_jobs = extract_job_attributes(path,key,ma_job_urls)


# In[63]:


len(ma_job_urls)


# In[64]:


ma_jobs


# 

# # Mongodb

# In[49]:


import pymongo
# set up the MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017")
# get the database you want to work with
db = client["DDR_Project"]
# get the collection you want to work with
collection = db["LinkedIn_Jobs"]
print(client.list_database_names())
print(db.list_collection_names())
x = collection.insert_many(ba_jobs)
print(x.inserted_ids)
x = collection.insert_many(ds_jobs)
print(x.inserted_ids)
x = collection.insert_many(da_jobs)
print(x.inserted_ids)
x = collection.insert_many(bi_jobs)
print(x.inserted_ids)
x = collection.insert_many(ma_jobs)
print(x.inserted_ids)


# In[ ]:





# In[ ]:





# In[ ]:




