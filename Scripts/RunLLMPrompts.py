""" Take the "summary prompts" for each article, and run them through a open source LLM to get article summaries """

#Representing file and directory paths
from pathlib import Path
#uses the fetch pdfs and mds scripts functions
from Fetch_PDFs_MDs_Daily import build_search_query
#function formatting, ->
from typing import List
#uses config.py to bring in necessary global arguments
from config import SUMMARIES_ROOT, SUMMARY_PROMPTS_ROOT, MODEL_ID, TEMPERATURE, MAX_NEW_TOKENS, GROQ_API_KEY, MARKDOWN_ROOT
from context import ctx
import ollama
from groq import Groq

def get_md_files(start_utc_time: str) -> List[str]:
    """ Pull the current md_files for chunking and embedding """

    md_folder = Path(MARKDOWN_ROOT) / start_utc_time
    # md_all_files = []
    # for file in Path(md_folder).glob("*.md"):
    #         md_all_files.append(str(file))
    # print(md_all_files)
    return [str(path) for path in md_folder.glob("*.md")]


def load_markdown(md_file: str) -> str:
    """ Read the Markdown files """

    return Path(md_file).read_text(encoding="utf-8")


#maybe function to clean the markdown text?


#maybe function to create prompt text?


if __name__ == "__main__":

    client = Groq(api_key = GROQ_API_KEY)

    md_files = get_md_files(ctx.start_utc_time)


    #create folder path for these generated article summaries
    summary_folder = Path(SUMMARIES_ROOT) / ctx.start_utc_time
    summary_folder.mkdir(parents=True, exist_ok=True)

    for md_file in md_files:
        
        #save the article summaries somewhere
        base = Path(md_file).stem
        summary_file = summary_folder / f"{base}.txt"

        raw_text = load_markdown(md_file)
        #clean raw markdown
        #create prompt template

        chat_completion = client.chat.completions.create(
            model= MODEL_ID,
            messages=[
                {"role": "user", "content": raw_text}
            ]
        )

        #save the LLM ouput to file OR Database??
        summary_file.write_text(chat_completion.choices[0].message.content, encoding="utf-8")
        print(f"Wrote: {summary_file}")
