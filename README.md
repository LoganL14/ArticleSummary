# Automating the collection of Arxiv Articles (pdfs), embedding model to summarize, and send scheduled emails to AI team

## Overview
This project automates the collection of scientific articles from https://arxiv.org, summarizes them by selecting representative chunks using embeddings and then generating summaries via an LLM. Then sends scheduled email updates to the AI team. The goal is to provide concise daily summaries of relevant research in AI, technology, and related fields.

## Project Steps

### Article Collection
- Query arXiv API for articles from two days ago (UTC).
- Parse XML response using BeautifulSoup.
- Extract PDF links and download articles into a structured folder system.

### Processing & Summarization
- Convert PDFs to Markdown using Docling
- Chunk text with LangChain.
- Compute embeddings for all chunks, calculate centroid per paper, select top‑k most representative chunks using cosine similarity.
- Summaries using top-k chunks and an appropriate model.

### Email Workflow
- Automate sending summarized articles via email to the AI team.
- Schedule tasks for daily execution.

## Tech Stack
- Python (requests, BeautifulSoup, pathlib, zoneinfo).
- LangChain for chunking and Hugging Face embedding model.
- Airflow or similar for scheduling.
- Git/GitHub for version control.

## Folder Structure
- downloaded_papers/ → PDFs
- downloaded_papers_md/ → Markdown conversions
- downloaded_embeddings/ → .npy embeddings + .jsonl metadata
- summary_prompts/ → prompt templates for LLM summarization


## Next Steps
- Integrate LLM summarization using saved prompts.
- Automate email dispatch with summaries.
- Improve chunking and embedding approaches, and enhance selection logic for summaries.
