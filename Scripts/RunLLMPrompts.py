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
import re 

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

# def clean_markdown_from_pdf(text: str) -> str:
#     """Fix common PDF→Markdown conversion artifacts while preserving structure."""
#     # 1) Merge paragraph breaks that split sentences (.,;: followed by 1–3 newlines + lowercase)
#     text = re.sub(r'([.,;:])\n{1,3}([a-z])', r'\1 \2', text)

#     # 2) De-hyphenate words broken across lines
#     text = re.sub(r'(\w+)-\n+(\w+)', r'\1\2', text)

#     # 3) Remove typical page headers/footers (arXiv headers; “Page X of Y”, etc.)
#     text = re.sub(r'\n\s*Page\s+\d+(?:\s+of\s+\d+)?\s*\n', '\n', text, flags=re.IGNORECASE)
#     text = re.sub(r'\narXiv:\S+\s*\n', '\n', text)  # basic arXiv header; keep it conservative

#     # 4) Normalize excessive blank lines (max two)
#     text = re.sub(r'\n{3,}', '\n\n', text)

#     # 5) Trim spaces before punctuation
#     text = re.sub(r'\s+([.,;:])', r'\1', text)

#     return text



#maybe function to create prompt text?

# def make_prompt(article_id: str, top_texts: list[str], article_url: str) -> str:
#     prompt = f"""TASK: Write a summary of the article ({article_id}) using ONLY the passages provided below.
# Guidelines (strict):
# 1) On the first line, output exactly (no changes): The article is available at: {article_url}
# 2) On the next line(s), output the summary text. (Around 150 words is solid length)
# 3) Paraphrase the passages, do NOT copy them verbatim.
# 3) Do NOT mention limitations or attempt to access the URL.

# PASSAGES: """
    
#     for i, text in enumerate(top_texts, 1):
#         prompt += f"Passage {i}:\n{text.strip()}\n\n"
#     return prompt




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
