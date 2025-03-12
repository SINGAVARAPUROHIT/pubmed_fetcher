📌 Project Overview
This project automates the extraction of research paper metadata from PubMed and processes the results using a Local LLM (Large Language Model) for structured output. The extracted details include:

PubMed ID
Title of Paper
Publication Date
Corresponding Author Email
The extracted data is saved in a CSV file using a GUI-based file selection dialog.

🛠️ Technologies Used
Python
Requests (for API calls to PubMed)
XML Parsing (for metadata extraction)
Transformers (Hugging Face) (for LLM-based text processing)
Tkinter (for GUI-based file saving)
📥 Installation Guide
Install Dependencies
Make sure you have Python installed (≥3.8). Then, install the required dependencies:

bash
Copy
Edit
pip install -r requirements.txt
 Run the Script
Execute the script to start fetching PubMed papers and saving results:

bash
Copy
Edit
python main.py
📝 How It Works
1️⃣ User enters a search query related to a research topic.
2️⃣ The script fetches PubMed papers matching the query.
3️⃣ It extracts metadata like the title, publication date, and author details.
4️⃣ A local LLM processes the metadata for structured output.
5️⃣ The extracted details are saved as a CSV file (location selected via GUI).

📌 Features
✅ Automates PubMed metadata retrieval
✅ Uses a Local LLM for text processing
✅ Extracts corresponding author emails
✅ Saves structured data in CSV format
✅ User-friendly GUI for file saving

🛠️ Configuration
If needed, you can modify the default number of results fetched by changing this line in main.py:


