""" Script to collect pdfs from articles posted 2 days ago. Put them into . /downloaded_papers folder"""

#uses config.py to bring in necessary global arguments
from config import BASE_URL, MAX_RESULTS, search_term, REQUEST_TIMEOUT, DATE_FMT_API, DOWNLOAD_ROOT
#lets you extract information from an API
from requests.exceptions import RequestException
import requests
#work with dates, +/-, etc
from datetime import datetime
#to pull from xml request, the data I need (PDFs)
from bs4 import BeautifulSoup
#representing file and directory paths
from pathlib import Path
from context import ctx
import time


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


def fetch_pdf_urls(search_query: str) -> list[str]:
    """Query arXiv and return PDF URLs only (no downloading)."""

    params = {
        "search_query": search_query,
        "max_results": MAX_RESULTS,
    }

    resp = requests.get(BASE_URL, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "xml")
    time.sleep(1)

    return [link["href"] 
            for link in soup.find_all("link") 
            if link.get("type") == "application/pdf"]


def download_pdfs(pdf_urls: list[str], start_utc_time: str) -> list[str]:
    """Download PDFs to disk and return local file paths."""

    download_folder = Path(DOWNLOAD_ROOT) / start_utc_time
    download_folder.mkdir(parents=True, exist_ok=True)

    local_paths = []

    for url in pdf_urls:
        filename = url.split("/")[-1] + ".pdf"
        fp_path = download_folder / filename

        if fp_path.exists():
            local_paths.append(str(fp_path))
            continue

        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(fp_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        local_paths.append(str(fp_path))

    return local_paths


if __name__ == "__main__":

    #Call the function to build the search query
    search_query = build_search_query(ctx.start_utc_dt, ctx.end_utc_dt)

    #Using the search query, fetch the pdf urls
    pdf_urls= fetch_pdf_urls(search_query)
    print(pdf_urls)
    
    #download the resulting pdfs, store the local path in "local_paths"
    local_paths = download_pdfs(pdf_urls, ctx.start_utc_time)
    #print(local_paths)