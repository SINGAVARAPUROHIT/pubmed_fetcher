import requests
import csv
import re
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog

def search_pubmed(query, retmax=5):
    """Search PubMed for papers matching the query and return PubMed IDs."""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmax": retmax, "retmode": "json"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_pubmed_metadata(pmid):
    """Fetch the metadata for a given PubMed ID using the EFetch API."""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {"db": "pubmed", "id": pmid, "retmode": "xml"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.text

def extract_details_from_metadata(metadata, pmid):
    """Extract details such as title, publication date, and corresponding author email from metadata."""
    details = {
        "pubmed_id": pmid,
        "title": None,
        "publication_date": None,
        "corresponding_author_email": None
    }

    try:
        root = ET.fromstring(metadata)

        # Extract Title
        title_elem = root.find(".//ArticleTitle")
        if title_elem is not None:
            details["title"] = title_elem.text

        # Extract Publication Date
        pub_date_elem = root.find(".//PubDate")
        if pub_date_elem is not None:
            year = pub_date_elem.find("Year")
            month = pub_date_elem.find("Month")
            day = pub_date_elem.find("Day")
            if year is not None:
                details["publication_date"] = f"{year.text}-{month.text if month is not None else '01'}-{day.text if day is not None else '01'}"

        # Extract Corresponding Author Email
        for affiliation in root.findall(".//Affiliation"):
            if affiliation.text:
                email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", affiliation.text)
                if email_match:
                    details["corresponding_author_email"] = email_match.group(0)
                    break

    except ET.ParseError as e:
        print(f"Error parsing XML for PubMed ID {pmid}: {e}")

    return details

def save_to_csv(data):
    """Save extracted PubMed data to a CSV file using a GUI save dialog."""
    if not data:
        print("No data extracted.")
        return

    # Initialize Tkinter properly and hide the root window
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)  # Ensure the dialog appears on top

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        title="Save CSV File"
    )

    if not file_path:
        print("Save operation canceled.")
        return

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"✅ Data successfully saved to: {file_path}")

def process_pubmed_papers():
    """Fetch and extract details for PubMed papers, then save results via GUI."""
    query = input("🔍 Enter your PubMed search query: ")
    num_papers = int(input("📄 Enter number of papers to fetch (default is 5): ") or 5)

    pubmed_ids = search_pubmed(query, retmax=num_papers)
    extracted_data = []

    for pmid in pubmed_ids:
        print(f"📑 Processing PubMed ID: {pmid}")
        metadata = fetch_pubmed_metadata(pmid)
        details = extract_details_from_metadata(metadata, pmid)

        if details["title"] is not None:
            extracted_data.append(details)
        else:
            print(f"⚠️ No details extracted for PubMed ID {pmid}.")

    save_to_csv(extracted_data)

# Run the process
process_pubmed_papers()
