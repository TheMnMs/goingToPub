import mysql.connector
from Bio import Entrez
import time

Entrez.email = "namita.ach04@gmail.com"

DB_CONFIG = {
    "host": "localhost",
    "user": "bob",
    "password": "youactuallythought",
    "database": "pubmed_db"
}

def connectDB():
    return mysql.connector.connect(**DB_CONFIG)

def makeTable():
    with connectDB() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS papers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    pmid VARCHAR(255) NOT NULL UNIQUE,
                    doi VARCHAR(255) UNIQUE
                )
            """)
            conn.commit()

def getDOI(query, max_results=10):
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    pmids = record["IdList"]
    
    dois = []
    for pmid in pmids:
        try:
            fetch_handle = Entrez.efetch(db="pubmed", id=pmid, rettype="xml", retmode="text")
            article_data = Entrez.read(fetch_handle)
            fetch_handle.close()
            
            # get the DOI
            article = article_data["PubmedArticle"][0]
            article_ids = article["MedlineCitation"]["Article"].get("ELocationID", [])
            doi = next((eid for eid in article_ids if eid.attributes.get("EIdType") == "doi"), "N/A")
            
            dois.append((pmid, doi))
            print(f"Retrieved DOI: {doi} for PMID: {pmid}")
            
            time.sleep(0.5)  # Avoid rate limits
            
        except Exception as e:
            print(f"Error fetching PMID {pmid}: {e}")

    return dois

def insertDB(pmid, doi):
    try:
        with connectDB() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO papers (pmid, doi) VALUES (%s, %s)", (pmid, doi))
                conn.commit()
    except mysql.connector.IntegrityError:
        print(f"Duplicate entry: PMID {pmid} already logged.")

def logDOI(query, max_results=10):
    makeTable()
    dois = getDOI(query, max_results)
    for pmid, doi in dois:
        insertDB(pmid, doi)
        print(f"Logged: PMID {pmid} → DOI {doi}")

logDOI("machine learning", max_results=20)
