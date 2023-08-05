#!/usr/bin/env python
# coding: utf-8

# In[248]:


import pandas as pd
import requests

from collections import Counter
from pathlib import Path
from requests_html import HTMLSession
from urllib.parse import urlparse

session = HTMLSession()


# In[260]:


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


# In[251]:


def get_page(url):
    page = session.get(url)
    #     try:
    #     page.html.render(reload=True)
    #     except:
    #         print('Page retrieval failed')
    return page.html


# In[269]:


def get_links_with_text(page, text, excluded_text):
    links = []
    excluded_links = []
    text_list = text.split(",")
    excluded_text_list = excluded_text.split(",")
    for term in text_list:
        term = term.strip()
        relative_links = page.find("a", containing=term)
        relative_excluded_links = page.find("a", containing=excluded_text)
        for link in relative_links:
            links.append(list(link.absolute_links)[0])
        for link in relative_excluded_links:
            excluded_links.append(list(link.absolute_links)[0])
    for term in excluded_text_list:
        term = term.strip()
        relative_excluded_links = page.find("a", containing=term)
        for link in relative_excluded_links:
            excluded_links.append(list(link.absolute_links)[0])
    counts = Counter(links)
    output = [
        value
        for value, count in counts.items()
        if count > 1 and value not in excluded_links
    ]
    return output


# In[263]:


def get_page_name(link):
    pl = urlparse(link)
    doc_name = pl[2].strip("/")
    page_name = doc_name.rsplit("/", 1)[-1]
    return page_name


# In[265]:


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


# In[274]:


def save_documents(config):
    for row in config:
        print()
        print("****************")
        print(row["institutional_investor"])
        print(row["folder_name"], "-", row["type"], ":")
        page = get_page(row["location"])
        links = get_links_with_text(
            page, row["terms_to_include"], row["terms_to_exclude"]
        )
        for link in links:
            save_file(link, row["folder_path"], row["type"])
    return "Completed"


# In[276]:


def test_fetch(config):
    for row in config:
        print()
        print("****************")
        print(row["institutional_investor"])
        print(row["folder_name"], "-", row["type"], ":")
        page = get_page(row["location"])
        links = get_links_with_text(
            page, row["terms_to_include"], row["terms_to_exclude"]
        )
        for link in links:
            print(f" - {link}")
    print(
        """\nThese documents have not been saved. Run "save_documents(config)" to save.\n
Note that only links to documents such as PDF files, Excel files and Word documents will be downloaded."""
    )


# In[ ]:
