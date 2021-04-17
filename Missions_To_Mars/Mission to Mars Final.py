#!/usr/bin/env python
# coding: utf-8

# In[75]:


# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd


# In[76]:


#pointing to the directory where chromedriver exists
executable_path = {"executable_path":"C:\\Users\\User\\documents\chromedriver"}
browser = Browser("chrome", **executable_path, headless = False)


# In[77]:


#Mars site URL #
mars_site_url = "https://redplanetscience.com/"
browser.visit(mars_site_url)

# Retrieve page with the requests module
response = requests.get(mars_site_url)

# Create BeautifulSoup object; parse with 'html.parser'
soup = bs(response.text, "lxml")


# In[78]:


# Examine the results, then determine element that contains sought info
print(soup.prettify())


# In[79]:


### MARS NEWS ###


# In[80]:


# Retrieve the latest element that contains news title and news_paragraph
news_title = soup.find('div', class_='content_title').find('').text


news_p = soup.find('div', class_='article_teaser_body').text



# Display scrapped data 
print(news_title)
print(news_p)


# In[81]:


### JPL MARS SPACE IMAGES ###


# In[82]:


featured_image_url = "https://spaceimages-mars.com/image/featured/mars3.jpg"
browser.visit(featured_image_url)


# In[83]:


### MARS FACTS ###


# In[102]:


url = "https://space-facts.com/mars/"
browser.visit(url)
# Use Pandas to "read_html" to parse the URL
tables = pd.read_html(url)
#tables
marsdf = tables[0]
marsdf


# In[85]:


### HEMISPHERES ###


# In[86]:


# Scrape Mars hemisphere title and image
mars_url='https://marshemispheres.com/'
browser.visit(mars_url)
html=browser.html
soup=bs(html,'html.parser')


# In[87]:


# Extract hemispheres item elements
mars_hems=soup.find('div',class_='collapsible results')
mars_item=mars_hems.find_all('div',class_='item')
hemisphere_image_urls=[]


# In[92]:


# Loop through each hemisphere item
for item in mars_item:
    # Error handling
    try:
        # Extract title
        hem=item.find('div',class_='description')
        title=hem.h3.text
        # Extract image url
        hem_url=hem.a['href']
        browser.visit(mars_url+hem_url)
        html=browser.html
        soup=bs(html,'html.parser')
        image_src=soup.find('li').a['href']
        if (title and image_src):
            # Print results
            print('-'*50)
            print(title)
            print(image_src)
        # Create dictionary for title and url
        hem_dict={
            'title':title,
            'image_url':image_src
        }
        hemisphere_image_urls.append(hem_dict)
    except Exception as e:
        print(e)


# In[103]:


# Create dictionary for all info scraped from sources above
mars_dictionary={
    "news_title":news_title,
    "news_p":news_p,
    "featured_image_url":featured_image_url,
    "fact_table":tables,
    "hemisphere_images":hemisphere_image_urls
}


# In[104]:


mars_dictionary


# In[ ]:




