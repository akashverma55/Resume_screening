import streamlit as st
import re 
import joblib
import nltk

nltk.download('punkt')
nltk.download('stopwords')

# loading the model and vectorizer
model = joblib.load('best_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Function to preprocess the text
def clean_resume(text):
    text = re.sub(r'http\S+\s', ' ', text)  # Remove URLs
    text = re.sub('RT|cc', ' ', text)  # Remove RT and cc
    text = re.sub('#\S+\s', ' ', text)  # Remove hashtags           
    text = re.sub('@\S+\s', ' ', text)  # Remove mentions
    text = re.sub('[%s]' % re.escape("""!"#$&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', text)  # Remove punctuation
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII characters
    text = re.sub('\s+'," ", text)  # Remove extra whitespace
    text = text.lower()
    return text

# website
st.title("Resume Classifier")
uploaded_file = st.file_uploader("Upload your resume", type=["txt","pdf"])

if uploaded_file is not None:
    try:
        resume_bytes = uploaded_file.read()
        resume_text = resume_bytes.decode("utf-8")
    except UnicodeDecodeError:
        resume_text = resume_bytes.decode("latin-1")

    cleaned_resume = clean_resume(resume_text)
    vactorized_resume = vectorizer.transform([cleaned_resume])
    prediction = model.predict(vactorized_resume)[0]

    job_label_mapping = {
        12: 'Data Science',
        26: 'HR',
        1: 'Advocate',
        38: 'Web Designing',
        29: 'Mechanical Engineer',
        35: 'Sales',
        24: 'Health and Fitness',
        9: 'Civil Engineer',
        28: 'Java Developer',
        6: 'Business Analyst',
        36: 'SAP Developer',
        2: 'Automation Testing',
        18: 'Electrical Engineering',
        31: 'Operations Manager',
        34: 'Python Developer',
        15: 'Devops Engineer',
        30: 'Network Security Engineer',
        32: 'PMO',
        13: 'Database',
        23: 'Hadoop',
        20: 'ETL developer',
        17: 'Dotnet Developer',
        5: 'Blockchain',
        37: 'Testing',
        14: 'Designer',
        27: 'Information-Technology',
        7: 'Business-Development',
        25: 'Healthcare',
        22: 'Fitness',
        11: 'Consultant',
        16: 'Digital-Media',
        8: 'Chef',
        21: 'Finance',
        19: 'Engineering',
        0: 'Accountant',
        10: 'Construction',
        33: 'Public-Relations',
        4: 'Banking',
        3: 'Aviation'
    }
    category_name = job_label_mapping.get(prediction, "Unknown Category")
    st.write(f"Category: {category_name}")
