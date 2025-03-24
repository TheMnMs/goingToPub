import mysql.connector
from Bio import Entrez
import time

Entrez.email = "namita.ach04@gmail.com"

# MySQL Database Config
DB_CONFIG = {
    "host": "localhost",
    "user": "bob",
    "password": "hahayouthought",
    "database": "pubmed_db"
}

def connectDB():
    return mysql.connector.connect(**DB_CONFIG)

def makeTable():
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pmid VARCHAR(255) NOT NULL,
            doi VARCHAR(255) UNIQUE
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def getDOI(query, max_results=10):
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    pmids = record["IdList"]
    
    dois = []
    for pmid in pmids:
        details = Entrez.efetch(db="pubmed", id=pmid, rettype="xml")
        data = Entrez.read(details)
        try:
            doi = next(
                (x["Identifier"] for x in data["PubmedArticle"][0]["PubmedData"]["ArticleIdList"] if x.attributes["IdType"] == "doi"), 
                None
            )
            if doi:
                dois.append((pmid, doi))
        except (KeyError, IndexError):
            pass
        
        time.sleep(0.5)  # Avoid API rate limits
    return dois

def insertDB(pmid, doi):
    conn = connectDB()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO papers (pmid, doi) VALUES (%s, %s)", (pmid, doi))
        conn.commit()
    except mysql.connector.IntegrityError:
        print(f"Duplicate entry: PMID {pmid} already logged.")
    cursor.close()
    conn.close()

def logDOI(query, max_results=10):
    makeTable()
    dois = getDOI(query, max_results)
    for pmid, doi in dois:
        insertDB(pmid, doi)
        print(f"Logged: PMID {pmid} → DOI {doi}")

logDOI("machine learning", max_results=20)
