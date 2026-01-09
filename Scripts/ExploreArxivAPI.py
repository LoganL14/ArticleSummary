import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path


base_url = "http://export.arxiv.org/api/query"


tz = ZoneInfo("UTC")
now_utc = datetime.now(tz) - timedelta(days=2)
twodaysago_midnight_utc = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
twodaysago_end_utc = now_utc.replace(hour=23, minute=59, second=59, microsecond=0)
# clean way to look at the day you are looking at
yday_label = str(twodaysago_midnight_utc.date())


#format for query
fmt = "%Y%m%d%H%M"
start_utc_format =  twodaysago_midnight_utc.strftime(fmt)
end_utc_format =  twodaysago_end_utc.strftime(fmt)
#print(start_utc_format)

time = "submittedDate:[{start_utc_formatted} TO {end_utc_formatted}]"

query = f"all:* AND {time}"
#print(query)
#"all:*+AND+submittedDate:[202512162300+TO+202512172300]"

params = {"search_query" : "submittedDate:[202512170000 TO 202512182359]" ,
          "max_results" : 20}

#date_query = f"submittedDate:[{start_utc_time} TO {end_utc_time}]"

# Make request using the search query found
def allarticles():
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    #print(response.text)
    
    #use soup so you can access just specific parts of the xml
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, "xml")
    all_entries = soup.find_all("entry") 
    #print(all_entries)
    for entry in all_entries:
        title = entry.find("title").text.strip()
        summary = entry.find("summary").text.strip()
        url = [link.get("href") for link in entry.find_all("link") if link.get("type") == "application/pdf"]
        date = entry.find("published").text.strip()
        category = [topic.get("term") for topic in entry.find_all("category")]
        authors = [a.find("name").text.strip() for a in entry.find_all("author")]
        comment = entry.find("arxiv:comment").text.strip() if entry.find("arxiv:comment") else None
        print("Title:", title)
        print("Authors:", authors)
        print("Summary:", summary[:50], "...")
        print("Date Published:", date)
        print("Category:", category)
        print("Url:", url)
        print("Comment:", comment)
        print("-" * 40)



allarticles()


#title
#authors
#summary/abstract
#url?

#category?
# cs 
# math
# physics
# astro-ph
# cond-mat
# gr-qc
# hep-ex
# hep-lat
# nlin
# nucl-ex
# q-bio
# q-fin
# stat
# #eess
# econ

#published date