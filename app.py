import streamlit as st
import spacy
import pdfplumber
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#do page setup
st.set_page_config(page_title="AI Resume Parser", page_icon="🤖")

#Load AI model
nlp=spacy.load("en_core_web_sm")

#Extract text from pdf
def get_text(file):
    text=""
    with pdfplumber.open(file)as pdf:
        for p in pdf.pages:
            if p.extract_text():
                text+=p.extract_text()
    return text
#extracting name using AI
def get_name(text):
    for ent in nlp(text).ents:
        if ent.label_=="PERSON":
            return ent.text
    return "Not found"
def get_email(text):
    pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
    match = re.search(pattern, text)
    return match.group() if match else "Not found"

def get_skills(text):
    skills=["Python programming","Java programming","SQL databases",
            "Power BI data visualization","Machine Learning",
            "Natural Language Processing","HTML web development",
            "CSS styling","Git version control","Data Analysis"]
    tfidf = TfidfVectorizer().fit_transform(skills + [text])
    sim = cosine_similarity(tfidf[-1:], tfidf[:-1]).flatten()
    return [skills[i] for i, s in enumerate(sim) if s > 0.1]
st.title("🤖 AI Resume Parser")
file=st.file_uploader("Upload Resume PDF",type="pdf")
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


if file and st.button("Analyze"):
    txt = get_text(file)
    st.success("Analysis Complete!")

    name = get_name(txt)
    email = get_email(txt)
    skills = get_skills(txt)
    job, score = job_match(txt)

    st.write("### 👤 Name")
    st.write(name)

    st.write("### 📧 Email")
    st.write(email)

    st.write("### 💻 Skills Detected")
    st.write(", ".join(skills) if skills else "No skills detected")

    st.write("### 🎯 Best Job Match")
    st.write(job)

    st.write("### 📊 Match Score")
    st.write(str(score) + " %")
