import os 
from dotenv import load_dotenv
load_dotenv()

# arXiv API & Request Settings
BASE_URL: str =  "https://export.arxiv.org/api/query"
MAX_RESULTS: int = 100
#could fill this (e.g., 'cat:cs.AI' or 'all:technology')
search_term: str | None = None
REQUEST_TIMEOUT: int = 60
 
# Date / Time
TZ_NAME: str = "UTC"         
DAYS_OFFSET: int = 15 #15       
DATE_FMT_API: str = "%Y%m%d%H%M"  # format arXiv expects in submittedDate rang
 
# Directories
DOWNLOAD_ROOT: str = "./downloaded_papers"         
MARKDOWN_ROOT: str = "./downloaded_papers_md"  
EMBEDDINGS_ROOT: str = "./downloaded_embeddings"
SUMMARY_PROMPTS_ROOT: str = "./summary_prompts"
SUMMARIES_ROOT: str = "./summarized_articles"
METADATA_ROOT: str = "./article_metadata"

# Chunking
MAX_CHARS: int = 2000
OVERLAP: int = 200
 
# Embedding 
#model with higher max tokens, 8192 tokens. 1024 dimension size
#EMB_MODEL_HUG = "BAAI/bge-m3"
EMB_MODEL_HUG = "google/embeddinggemma-300m"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMB_MODEL = "gemini-embedding-001"
EMBED_MODEL = "all-MiniLM-L6-v2"  #sentence transformer model
 
#LLM Summarization
MODEL_ID = "llama-3.3-70b-versatile"
# 30 requests per min, 1000 requests per day, 12k requests per day, 12k tokens per min, 100k tokens per day
TEMPERATURE = 0
MAX_NEW_TOKENS = 250
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
#MODEL_ID = " llama-3.1-8b-instant"
# 30 requests per min, 14400 requests per day, 14.4k requests per day, 6k tokens per min 500k tokens per day
 
#Sending emails
#SMTP_SERVER = "smtp.gmail.com" or "smtp.comcast.net" or "smtp.office365.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # OR 465?
USERNAME = "logan.laszewski@gmail.com"
PASSWORD = os.getenv("PASSWORD")
RECEIVER = ["logan.laszewski@comcast.net", "llaszewski@elon.edu"]