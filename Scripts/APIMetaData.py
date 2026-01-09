"""This script builds metadata for each article using arxiv API """

import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
from config import BASE_URL, MAX_RESULTS, search_term, REQUEST_TIMEOUT, DATE_FMT_API, DOWNLOAD_ROOT
import time
#use soup so you can access just specific parts of the xml
from bs4 import BeautifulSoup
from context import ctx

def build_search_query(start_utc_dt: datetime, end_utc_dt : datetime, search_term = None) -> str:
    """Build a search query with date range and other information (optional).
    Returns:
        str: Formatted search query. In a format the API accepts."""

    #format the dates for query. Ex) 202512170000
    start_utc_time =  start_utc_dt.strftime(DATE_FMT_API)
    end_utc_time  =  end_utc_dt.strftime(DATE_FMT_API)
    
    #build the date query. Ex) submittedDate:[202512170000 TO 202512180000] 
    date_query = f"submittedDate:[{start_utc_time} TO {end_utc_time}]"
    
    #check if search term is added to create full query. Otherwise, just the date query
    if search_term:
        search_query = f"{search_term} AND {date_query}"
        return search_query

    else:
        search_query = date_query
        return search_query


def metadata(search_query: str):
    """Build formatted metadata for each article. Title, Authors, Summary, Date, Category, Url, Comments"
        Returns: Metadata formatted for use in database"""
    
    params = {
        "search_query": search_query,
        "max_results": MAX_RESULTS,
    }

    resp = requests.get(BASE_URL, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "xml")
    time.sleep(1)
    
    articles = []
    for entry in soup.find_all("entry"):
        title = entry.find("title").text.strip()
        summary = entry.find("summary").text.strip()
        url = [link.get("href") for link in entry.find_all("link") if link.get("type") == "application/pdf"]
        date = entry.find("published").text.strip()
        category = [topic.get("term") for topic in entry.find_all("category")]
        authors = [a.find("name").text.strip() for a in entry.find_all("author")]
        comment = entry.find("arxiv:comment").text.strip() if entry.find("arxiv:comment") else None
            
        article = {"Title": title, "Authors": authors,"Summary": summary,
                    "Date Published": date, "Category": category,
                    "Url": url, "Comment": comment}
        articles.append(article)
    
    return articles
        # print("Title:", title)
        # print("Authors:", authors)
        # print("Summary:", summary[:50], "...")
        # print("Date Published:", date)
        # print("Category:", category)
        # print("Url:", url)
        # print("Comment:", comment)
        # print("-" * 40)



if __name__ == "__main__":

    search_query = build_search_query(ctx.start_utc_dt, ctx.end_utc_dt)
    
    metadata = metadata(search_query)
    print(metadata)
