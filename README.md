# chatbot-para-answers
a chatbot which answers in paragraph of keyword from user.

# 🤖 S3-Powered PDF Chatbot

A FastAPI-based chatbot that take input questions in form of keyword and answer it in paragraph of keyword using PDF files stored in an AWS S3 bucket — without downloading them to disk.

---

## 🚀 Features

- ✅ **Cloud-Native**: Reads PDFs directly from S3.
- ✅ **FastAPI Framework**: Lightweight and high-performance.
- ✅ **PDF Text Extraction**: Handles multiple files inside S3 folders.
- ✅ **User Query Matching**: Returns the most relevant answer from the PDF data.

---

## 📁 Project Structure

```
chatbot/
│
├── bot.py             # Main application code
├── requirements.txt   # All Python dependencies
└── README.md          # You're here!
```

---

## 🧪 How It Works

1. Connects to AWS S3 using credentials.
2. Reads and extracts text from all PDFs inside a specified bucket folder.
3. Waits for user input via a web form.
4. Searches the most relevant matching content from PDFs.
5. Displays the answer directly in the browser.

---

## 🔧 Prerequisites

- Python 3.12+
- AWS credentials (with S3 read permissions)
- PDF files stored in an S3 bucket

---

## ⚙️ Setup & Run

```bash
# Clone the repo
git clone https://github.com/your-username/pdf-s3-chatbot.git
cd pdf-s3-chatbot

# Create and activate a virtual environment
python3 -m venv chatbot-env
source chatbot-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the chatbot
python bot.py
```

Visit: [http://localhost:8000](http://localhost:8000)

---

## 📦 Dependencies

Check `requirements.txt` for the full list of packages.

---

## 🛡️ License

MIT © 2025 [Your Name]
