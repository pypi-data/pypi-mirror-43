#!/usr/bin/env python
# coding: utf-8

# In[183]:


import pandas as pd
import requests

from collections import Counter
from pathlib import Path
from requests_html import HTMLSession
from urllib.parse import urlparse

session = HTMLSession()


# In[147]:


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


# In[149]:


def get_page(url):
    page = session.get(url)
    #     try:
    #     page.html.render(reload=True)
    #     except:
    #         print('Page retrieval failed')
    return page.html


# In[151]:


x = [1, 2, 2, 2, 3, 4, 5, 6, 6, 7]
counts = Counter(x)
output = [value for value, count in counts.items() if count > 1]
output


# In[176]:


def get_links_with_text(page, text):
    links = []
    text_list = text.split(",")
    for term in text_list:
        term = term.strip()
        relative_links = page.find("a", containing=term)
        for link in relative_links:
            links.append(list(link.absolute_links))
    return list(set([link.pop() for link in links]))


# In[163]:


def get_page_name(link):
    pl = urlparse(link)
    doc_name = pl[2].strip("/")
    page_name = doc_name.rsplit("/", 1)[-1]
    return page_name


# In[180]:


def save_file(link, folder_path, resource_type):
    excluded_filetypes = ["html"]
    folder_path.mkdir(parents=True, exist_ok=True)
    filename = folder_path / get_page_name(link)
    doc = session.get(link)
    file_type = doc.headers["content-type"].rsplit("/", 1)[-1]
    if file_type not in excluded_filetypes:
        filename = filename.with_suffix(f".{file_type}")
        if not filename.exists():
            filename.write_bytes(doc.content)
            print("New file: ", filename.name)
        else:
            print("Existing file: ", resource_type, filename.name)
        return "Success"


# In[168]:


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


# In[193]:


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
    print(
        """\nThese documents have not been saved. Run "save_documents(config)" to save.\n
Note that only links to documents such as PDF files, Excel files and Word documents will be downloaded."""
    )


# In[ ]:
