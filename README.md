# goingToPub
we will figure out how to use pubmed API to kick out the papers that were retracted 


## What namita did
- sh -c "(wget -qO- https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"
    - to get edirect in terminal
- haha sike but that didn't work properly so i did sudo apt isntall only
    - sudo apt update
    - sudo apt install ncbi-entrez-direct
- haan then check if it's installed
    - efetch -version
 - boom ba da bam it is set up
 - next we try some sample queries
    - esearch -db pubmed -query "genome sequencing" | efetch -format medline (ARTICLES ON A TOPIC)
      ![image](https://github.com/user-attachments/assets/99ff8647-901a-461d-8184-75c6209089b2)
    - einfo -db pubmed (INFO ABOUT PUBMED) (but i failed)
      ![image](https://github.com/user-attachments/assets/c18535ba-ebda-4be6-93c8-90609da661d2)
      - but i did not stop
      - i was able to access the xml though
      - it was a server issue i think

SO basically,

### **Full Table of PubMed EDirect Query Methods**
| **Query**                                  | **Why to Use**                                                      | **Example** |
|--------------------------------------------|----------------------------------------------------------------------|-------------|
| `einfo -db pubmed`                         | Get metadata about the PubMed database, including available fields.  | `einfo -db pubmed` |
| `esearch -db pubmed -query "cancer"`       | Search for articles on a topic and return the count.                 | `esearch -db pubmed -query "cancer"` |
| `esearch -db pubmed -query "COVID-19" | efetch -format uid` | Get a list of PubMed IDs (PMIDs) for articles matching a query. | `esearch -db pubmed -query "COVID-19" | efetch -format uid` |
| `esearch -db pubmed -query "AI in radiology" | efetch -format abstract` | Fetch abstracts of articles from PubMed. | `esearch -db pubmed -query "AI in radiology" | efetch -format abstract` |
| `efetch -db pubmed -id 12345678 -format xml` | Fetch full metadata for a specific article using its PubMed ID (PMID). | `efetch -db pubmed -id 12345678 -format xml` |
| `esearch -db pubmed -query "machine learning" | elink -target pmc` | Find full-text articles available in PubMed Central (PMC). | `esearch -db pubmed -query "machine learning" | elink -target pmc` |
| `elink -db pubmed -id 12345678 -target pmc` | Find the full-text version of a specific article if available. | `elink -db pubmed -id 12345678 -target pmc` |
| `esearch -db pubmed -query "CRISPR" | efetch -format medline` | Fetch results in **Medline format** for easy parsing. | `esearch -db pubmed -query "CRISPR" | efetch -format medline` |
| `esearch -db pubmed -query "Alzheimer's" | efetch -format json` | Fetch results in **JSON format** for use in scripts. | `esearch -db pubmed -query "Alzheimer's" | efetch -format json` |
| `esearch -db pubmed -query "cancer" | efetch -format docsum` | Get **summary information** for each article (title, journal, etc.). | `esearch -db pubmed -query "cancer" | efetch -format docsum` |
| `esearch -db pubmed -query "gene therapy" | efetch -format gb` | Fetch results in **GenBank format** (useful for genetic studies). | `esearch -db pubmed -query "gene therapy" | efetch -format gb` |
| `esearch -db pubmed -query "neuroscience" | efetch -format csv` | Get results in **CSV format** for easy spreadsheet use. | `esearch -db pubmed -query "neuroscience" | efetch -format csv` |
| `esearch -db pubmed -query "COVID-19" | efetch -format xml > covid_papers.xml` | Save output as an XML file for structured data processing. | `esearch -db pubmed -query "COVID-19" | efetch -format xml > covid_papers.xml` |
| `esearch -db pubmed -query "diabetes" | efetch -format abstract > diabetes.txt` | Save abstracts to a text file. | `esearch -db pubmed -query "diabetes" | efetch -format abstract > diabetes.txt` |
| `esearch -db pubmed -query "lung cancer" | head -20` | Limit results to the **first 20 articles**. | `esearch -db pubmed -query "lung cancer" | head -20` |
| `esearch -db pubmed -query "mental health" | efetch -format abstract | grep "2024"` | Get only papers **published in 2024**. | `esearch -db pubmed -query "mental health" | efetch -format abstract | grep "2024"` |
| `while true; do esearch -db pubmed -query "mRNA vaccine" | efetch -format abstract; sleep 3600; done` | Continuously **stream** the latest research every hour. | `while true; do esearch -db pubmed -query "mRNA vaccine" | efetch -format abstract; sleep 3600; done` |




# Biopython Entrez Guide

## Introduction
Biopython's `Entrez` module provides a powerful interface to the NCBI Entrez databases, allowing users to programmatically search, fetch, and analyze biomedical literature and other biological data. This guide covers installation, basic queries, and fetching article details from PubMed using `Entrez`.

## Installation
To use the `Entrez` module, install Biopython using pip:

```sh
pip install biopython
```

## Setting Up Entrez
NCBI requires users to provide an email address when making queries. Set your email before making requests:

```python
from Bio import Entrez
Entrez.email = "your_email@example.com"  # Replace with your email
```

## Searching PubMed
You can search PubMed for articles on a specific topic using `esearch`:

```python
handle = Entrez.esearch(db="pubmed", term="machine learning", retmax=10, retmode="json")
record = handle.read()
print(record)
```

- `db="pubmed"`: Specifies PubMed as the target database.
- `term="machine learning"`: The query to search for. To fetch retracted publication use: ```'"retracted publication"cancer'```
- `retmax=10`: Maximum number of results to return.
- `retmode="json"`: Returns results in JSON format.

## Fetching Article Details
Once you obtain a PubMed ID (PMID), you can fetch detailed information using `efetch`:

```python
handle = Entrez.efetch(db="pubmed", id="12345678", retmode="xml")
xml_data = handle.read()
print(xml_data)
```

- Replace `12345678` with the actual PMID of the paper you want to fetch.
- `retmode="xml"` returns structured data that can be parsed.

## Extracting Titles, Abstracts, and Authors
To extract specific details, use the `xml.etree.ElementTree` module:

```python
import xml.etree.ElementTree as ET

root = ET.fromstring(xml_data)
title = root.find(".//ArticleTitle").text
abstract = root.find(".//AbstractText").text

print(f"Title: {title}")
print(f"Abstract: {abstract}")
```

## Retrieving Retracted Papers
You can filter and fetch retracted papers using:

```python
query = '"retracted publication"[Publication Type]'
handle = Entrez.esearch(db="pubmed", term=query, retmax=5, retmode="json")
record = handle.read()
print(record)
```

This will return the PubMed IDs of retracted papers, which can be fetched using `efetch`.

For more details, refer to the [Biopython Entrez Documentation](https://biopython.org/wiki/Entrez).

