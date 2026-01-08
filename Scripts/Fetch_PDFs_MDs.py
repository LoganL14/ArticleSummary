""" Script to collect pdfs from articles posted 2 days ago. Put them into . /downloaded_papers folder
    Also, take the pdfs and convert them into markdown files. Put them into . /downloaded_papers_md folder"""

#uses config.py to bring in necessary global arguments
from config import BASE_URL, MAX_RESULTS, search_term, REQUEST_TIMEOUT, TZ_NAME, DAYS_OFFSET, DATE_FMT_API, DOWNLOAD_ROOT, MARKDOWN_ROOT
#lets you extract information from an API
from requests.exceptions import RequestException
import requests
#work with dates, +/-, etc
from datetime import datetime
#function formatting, -> 
from typing import Iterable
#to pull from xml request, the data I need (PDFs)
from bs4 import BeautifulSoup
#representing file and directory paths
from pathlib import Path
#docling to go from PDFs to md
from docling.document_converter import DocumentConverter
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


def fetch_papers(search_query: str, start_utc_time: str):
    """Using search_query, get all (up to "MAX_RESULTS") papers from "DAYS_OFFSET" days ago. 
    Using the result, get PDFs for each one and download locally in "./downloaded_papers" folder. 
    Returns:
        Folder full of the articles for this search."""
    
    #set up parameters which specify search
    params = {"search_query" : search_query,
          "max_results" : MAX_RESULTS}
    
    #send request
    resp = requests.get(BASE_URL, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    
    #parses the XML string into a navigable tree
    soup = BeautifulSoup(resp.text, "xml")
    
    #give me every <link> tag in the entire document
    all_entries = soup.find_all('link')
    
    #extracts only those <link>s whose type="application/pdf", returning a list of PDF URLs (https://arxiv.org/pdf/2512.12345v1)
    # i['href'] pulls the URL out of the attribute
    all_href_links = [i['href'] for i in all_entries if i.get('type') == 'application/pdf']
    
    #download the papers into specific folder 
    download_folder = Path(DOWNLOAD_ROOT) / start_utc_time
    download_folder.mkdir(parents=True, exist_ok=True)
    
    #naming each pdf that is downloaded
    resultspdf = []
    for url in all_href_links:
        filename = url.split('/')[-1] + '.pdf'
        fp_path = download_folder / filename
        print(f"Attempting to download {filename} to {fp_path}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
    
        #write the content to a file in chunks
            with open(fp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Successfully downloaded: {filename}")
            resultspdf.append(str(fp_path))
        except RequestException as e:
            print(f"An error occurred during download: {e}")
    return resultspdf


def parse_pdf_to_markdown(resultspdf: Iterable[str], start_utc_time: str) -> list[str]:
    """Convert the batch of PDF files to Markdown and save them in "./download_folder_md" folder.
    Returns:
        list[str]: Paths to successfully written Markdown files."""
    
    download_folder_md = Path(MARKDOWN_ROOT) / start_utc_time
    download_folder_md.mkdir(parents=True, exist_ok=True)
    converter = DocumentConverter()
    downloadedmd = []
    for fp_path in resultspdf:
        base = Path(fp_path).stem
        md_path = download_folder_md / f"{base}.md"
        try: 
            md_text = converter.convert(fp_path)
            md_final = md_text.document.export_to_markdown()
            md_path.write_text(md_final, encoding="utf-8")
            print(f"Saved Markdown: {md_path}")
            downloadedmd.append(str(md_path))
        except Exception as e:
            print(f"Failed to save Markdown for {fp_path}: {e}")
    return downloadedmd
    

if __name__ == "__main__":

    #Call the function to build the search query
    search_query = build_search_query(ctx.start_utc_dt, ctx.end_utc_dt)

    #download the resulting pdfs, store the pdfs in a list "resultspdf"
    resultspdf = fetch_papers(search_query, ctx.start_utc_time)

    #download the resulting md files, store in a list "resultsmd"
    resultsmd = parse_pdf_to_markdown(resultspdf, ctx.start_utc_time)