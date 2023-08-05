#!/usr/bin/env python
# coding: utf-8

# In[34]:


import pandas as pd
import requests

from pathlib import Path
from requests_html import HTMLSession
from urllib.parse import urlparse

session = HTMLSession()


# In[57]:


def make_path(base_path, config_file, institutional_investor):
    config_df = pd.read_excel(config_file)
    config_df = config_df[config_df.institutional_investor == institutional_investor]
    config_df["folder_path"] = config_df.apply(
        lambda row: Path.cwd()
        / base_path
        / row.institutional_investor
        / row.folder_name
        / row.type.lower(),
        axis=1,
    )
    display(config_df)
    return config_df.to_dict(orient="records")


# In[43]:


def get_page(url):
    page = session.get(url)
    #     try:
    #     page.html.render(reload=True)
    #     except:
    #         print('Page retrieval failed')
    return page.html


# In[49]:


def get_links_with_text(page, text):
    links = []
    relative_links = page.find("a", containing=text)
    for link in relative_links:
        links.append(link.absolute_links)
    return list(set([link.pop() for link in links]))


# In[51]:


def get_page_name(link):
    pl = urlparse(link)
    doc_name = pl[2].strip("/")
    page_name = doc_name.rsplit("/", 1)[-1]
    return page_name


# In[53]:


def save_file(link, folder_path, resource_type):
    folder_path.mkdir(parents=True, exist_ok=True)
    filename = folder_path / get_page_name(link)
    doc = session.get(link)
    file_type = doc.headers["content-type"].rsplit("/", 1)[-1]
    filename = filename.with_suffix(f".{file_type}")
    if not filename.exists():
        filename.write_bytes(doc.content)
        print("New file: ", filename.name)
    else:
        print("Existing file: ", resource_type, filename.name)
    return "Success"


# In[58]:


def save_documents(config):
    for row in config:
        print()
        print("****************")
        print(row["institutional_investor"])
        print(row["folder_name"], "-", row["type"], ":")
        page = get_page(row["location"])
        links = get_links_with_text(page, row["search_terms"])
        for link in links:
            save_file(link, row["folder_path"], row["type"])
    return "Completed"


# In[73]:


def test_fetch(config):
    for row in config:
        print()
        print("****************")
        print(row["institutional_investor"])
        print(row["folder_name"], "-", row["type"], ":")
        page = get_page(row["location"])
        links = get_links_with_text(page, row["search_terms"])
        for link in links:
            print(f" - {link}")
    return 'These documents have not been saved. Run "save_documents(config)" to save'


# In[ ]:
