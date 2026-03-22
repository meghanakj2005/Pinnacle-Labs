import spacy
import pdfplumber
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
nlp=spacy.load("en_core_web_sm")
def extract_text_from_pdf(file_path):
    text=""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text+=page.extract_text()
    return text  

def extract_name(text):
    doc=nlp(text)
    for ent in doc.ents:
        if ent.label_=="PERSON":
            return ent.text
    return "Name not found" 
def extract_email(text):
    pattern=r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    match=re.search(pattern,text)
    if match:
        return match.group()
    return "Email not found"
def extract_skills_ai(resume_text):
    skills_db=["Python programming","Java programming","SQl databases","Power BI data visulization","Machine Learning","Natural Language Processing","HTML web development","CSS styling","Git version control","Data Analyisis"]
    documents=skills_db+[resume_text]
    tfidf=TfidfVectorizer()
    tfidf_matrix=tfidf.fit_transform(documents)
    resume_vector=tfidf_matrix[-1]
    skills_vectors=tfidf_matrix[:-1]
    similarity=cosine_similarity(resume_vector,skills_vectors)
    found_skills=[]
    for i,score in enumerate(similarity[0]):
        if score>0.1:
            found_skills.append(skills_db[i])
        return found_skills  
def job_match(text):
    jobs = [
        "Python developer with machine learning and data science",
        "Java backend developer with spring boot",
        "Web developer with HTML CSS JavaScript React",
        "Data analyst with SQL Power BI Python",
        "Cybersecurity analyst with network security"
    ]

    tfidf = TfidfVectorizer().fit_transform(jobs + [text])
    scores = cosine_similarity(tfidf[-1:], tfidf[:-1]).flatten()

    best_index = scores.argmax()
    best_job = jobs[best_index]
    match_percent = round(scores[best_index] * 100, 2)

    return best_job, match_percent
      


 
