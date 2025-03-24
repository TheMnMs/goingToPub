import csv
from Bio import Entrez
import time

Entrez.email = "namita.ach04@gmail.com"

# CSV file
CSV_FILE = "doi_log.csv"
HEADER = ["PubMed_ID", "DOI"]

try:
    with open(CSV_FILE, "x", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
except FileExistsError:
    pass  # File already exists, continue appending data


def logDOI(query, max_results=500):
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    
    pmids = record["IdList"]
    print(f"Found {len(pmids)} articles for query: {query}")
    
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        
        for pmid in pmids:
            try:
                fetch_handle = Entrez.efetch(db="pubmed", id=pmid, rettype="xml", retmode="text")
                article_data = Entrez.read(fetch_handle)
                fetch_handle.close()
                
                # Extract DOI
                article = article_data["PubmedArticle"][0]
                article_ids = article["MedlineCitation"]["Article"]["ELocationID"]
                doi = next((eid for eid in article_ids if eid.attributes.get("EIdType") == "doi"), "N/A")
                
                # Log to CSV
                writer.writerow([pmid, doi])
                print(f"Logged DOI: {doi} for PMID: {pmid}")
                time.sleep(0.5)  # To avoid rate limits
            
            except Exception as e:
                print(f"Error fetching PMID {pmid}: {e}")


logDOI("machine learning", max_results=10)
