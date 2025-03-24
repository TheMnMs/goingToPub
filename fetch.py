from Bio import Entrez
import json
import time
import xml.etree.ElementTree as ET

Entrez.email = "your_email@example.com"  # Required for NCBI API

def fetch_retracted_pmids(count=5):
    """Fetch PMIDs of retracted papers from PubMed."""
    query = '"retracted publication"[Publication Type]'
    handle = Entrez.esearch(db="pubmed", term=query, retmax=count, retmode="json")
    response = handle.read()
    record = json.loads(response)
    return record.get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(pmid):
    """Fetch details of a PubMed article, including title, abstract, and retraction status."""
    try:
        handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
        xml_data = handle.read()
        root = ET.fromstring(xml_data)

        # Extract article title
        title_element = root.find(".//ArticleTitle")
        title = title_element.text if title_element is not None else "No Title Found"

        # Extract abstract
        abstract_element = root.find(".//AbstractText")
        abstract = abstract_element.text if abstract_element is not None else "No Abstract Available"

        # Extract authors
        authors = []
        for author in root.findall(".//Author"):
            last_name = author.find("LastName")
            fore_name = author.find("ForeName")
            full_name = f"{fore_name.text if fore_name is not None else ''} {last_name.text if last_name is not None else ''}".strip()
            if full_name:
                authors.append(full_name)

        # Extract journal name
        journal_element = root.find(".//Journal/Title")
        journal = journal_element.text if journal_element is not None else "Unknown Journal"

        # Generate official PubMed link
        pubmed_link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

        # Check retraction status
        retracted = False
        retraction_type = "Not Retracted"
        for pub_type in root.findall(".//PublicationType"):
            if pub_type.text == "Retracted Publication":
                retracted = True
                retraction_type = "Retracted Publication"
            if pub_type.text == "Retraction of Publication":
                retracted = True
                retraction_type = "Retraction Notice"

        return {
            "pmid": pmid,
            "title": title,
            "abstract": abstract,
            "authors": authors,
            "journal": journal,
            "retracted": retracted,
            "retraction_type": retraction_type,
            "pubmed_link": pubmed_link
        }

    except Exception as e:
        return {"pmid": pmid, "error": str(e)}

# Fetch retracted PMIDs
retracted_pmids = fetch_retracted_pmids(5)

# Fetch paper details for each
paper_details = []
for pmid in retracted_pmids:
    paper_details.append(fetch_paper_details(pmid))
    time.sleep(1)  # Prevent hitting API rate limits

# Print results
for paper in paper_details:
    print(json.dumps(paper, indent=4))
