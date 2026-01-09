""" Script to take downloaded pdfs and run them through an LLM model to get summaries/metadata.
Downloaded metadata saved to ./article_metadata folder. """

#uses config.py to bring in necessary global arguments
from config import MODEL_ID
#representing file and directory paths
from context import ctx
from groq import Groq
from config import MODEL_ID, GROQ_API_KEY, METADATA_ROOT, DOWNLOAD_ROOT
import time
#representing file and directory paths
from pathlib import Path
from FetchPDFs import build_search_query, fetch_pdf_urls
from urllib.parse import urlparse


def get_pdf_files(start_utc_time: str) -> list[str]:
    """ Get list of pdf files for a given run date """

    pdf_folder = Path(DOWNLOAD_ROOT) / start_utc_time
    return [str(fp) for fp in pdf_folder.glob("*")]


def make_LLM_prompt(pdf: str) -> str:
    """ Take in a pdf file, and create a prompt for the LLM model to summarize the article """

    prompt = f"""TASK: Extract metadata from this academic paper - {pdf} . Return only a valid JSON object. 
    Do not include markdown code fences, backticks, or any explanatory text.

    Example output:
    {{
        "title": "Transformer Models for Natural Language Processing",
        "authors": ["John Doe", "Jane Smith"],
        "topics": ["NLP", "Deep Learning"],
        "key_contributions": "Introduced novel attention mechanism for sequence modeling",
        "pdf_url": "{pdf}"
    }}"""

    return prompt


def run_LLM_summarization(prompt: str) -> str:
    """ Run the LLM model to get summaries for each article prompt """

    chat_completion = client.chat.completions.create(
            model= MODEL_ID,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    time.sleep(1.5)
    
    return(chat_completion.choices[0].message.content)


def save_metadata(pdf: str, metadata: str):
    """ Save the metadata returned from the LLM to a file """

    base = Path(pdf).stem
    metadata_file = metadata_folder / f"{base}.json"
    metadata_file.write_text(metadata, encoding="utf-8")
    #print(f"Wrote: {metadata_file}")


if __name__ == "__main__":

    client = Groq(api_key = GROQ_API_KEY)
    metadata_folder = Path(METADATA_ROOT) / ctx.start_utc_time
    metadata_folder.mkdir(parents=True, exist_ok=True)

    #search_query = build_search_query(ctx.start_utc_dt, ctx.end_utc_dt)
    #pdf_urls = fetch_pdf_urls(search_query)
    
    pdf_urls = get_pdf_files(ctx.start_utc_time)
    pdf_urls = pdf_urls[:50]  #limit to first 50 for testing
    
    for pdf in pdf_urls:
        #creates the LLM prompt for each pdf
        prompt = make_LLM_prompt(pdf)
        #runs the LLM summarization function
        metadata = run_LLM_summarization(prompt)
        #downloads metadata to json files
        save_metadata(pdf, metadata)
