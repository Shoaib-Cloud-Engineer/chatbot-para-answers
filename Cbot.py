from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import boto3
from io import BytesIO
import PyPDF2
import uvicorn
import difflib

app = FastAPI()

# ===== AWS + S3 Configuration =====
AWS_ACCESS_KEY_ID = "paste here"
AWS_SECRET_ACCESS_KEY = "paste here"
REGION_NAME = "us-east-1"
BUCKET_NAME = "botchat-bucket-1"
FOLDER_PREFIX = "chatbot/"  # Include trailing slash if it's a folder

# ===== Initialize S3 Client =====
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)

# ===== List All PDFs in the Folder =====
def list_pdf_keys(bucket: str, prefix: str):
    keys = []
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if key.lower().endswith(".pdf"):
                keys.append(key)
    return keys

# ===== Read PDF Content from S3 =====
def read_pdf_from_s3(bucket: str, key: str) -> str:
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        file_stream = BytesIO(response["Body"].read())
        reader = PyPDF2.PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        return f"Error reading {key}: {str(e)}"

# ===== Search with Fuzzy Matching =====
def search_query_in_pdfs(query: str) -> str:
    pdf_keys = list_pdf_keys(BUCKET_NAME, FOLDER_PREFIX)
    if not pdf_keys:
        return "No PDFs found in the folder."

    matched_paragraphs = []

    for key in pdf_keys:
        text = read_pdf_from_s3(BUCKET_NAME, key)
        if "Error" in text:
            continue

        paragraphs = text.split("\n\n")
        for para in paragraphs:
            ratio = difflib.SequenceMatcher(None, query.lower(), para.lower()).ratio()
            if ratio > 0.4 or any(word in para.lower() for word in query.lower().split()):
                matched_paragraphs.append(f"<b>{key}</b>: {para.strip()}")

    if matched_paragraphs:
        return "<br><br>".join(matched_paragraphs)
    else:
        return f"❌ No relevant content found for: '{query}'"

# ===== Web UI =====
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>S3 PDF Chatbot</title>
        </head>
        <body style="font-family: Arial; text-align: center; padding-top: 50px;">
            <h2>Ask a Question</h2>
            <form action="/ask" method="post">
                <input type="text" name="query" style="width: 300px; padding: 10px;" placeholder="Enter your question..." required />
                <br><br>
                <input type="submit" value="Ask" style="padding: 10px 20px;" />
            </form>
        </body>
    </html>
    """

@app.post("/ask", response_class=HTMLResponse)
async def ask(query: str = Form(...)):
    answer = search_query_in_pdfs(query)
    return f"""
    <html>
        <head><title>Answer</title></head>
        <body style="font-family: Arial; text-align: center; padding-top: 50px;">
            <h2>Answer</h2>
            <p><b>Question:</b> {query}</p>
            <p><b>Response:</b><br> {answer}</p>
            <br><a href="/">🔙 Ask another</a>
        </body>
    </html>
    """
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
