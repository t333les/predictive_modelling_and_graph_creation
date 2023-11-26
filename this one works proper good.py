import pandas as pd
import re
import datetime

# Load the data
data = pd.read_json('clinical_trials_data_final.json')

# Handle missing values
data.dropna(subset=['NCTId'], inplace=True)  # Remove rows with missing NCTId
data.fillna('', inplace=True)  # Fill other missing values with empty strings

# Convert date columns to datetime objects
date_columns = ['Study First Post Date', 'Completion Date']
for col in date_columns:
    data[col] = pd.to_datetime(data[col], errors='coerce')
    data[col] = data[col].dt.strftime('%Y-%m-%d')

# Text data cleaning
text_columns = ['Brief Title', 'Eligibility', 'Location', 'Condition']
for col in text_columns:
    data[col] = data[col].str.lower()  # Convert to lowercase
    data[col] = data[col].apply(
        lambda x: re.sub(r'[^a-zA-Z\s,]', '', x).strip())  # Remove special characters and strip spaces

# Handle 'Enrollment' column
data['Enrollment'] = data['Enrollment'].str.replace(',', '', regex=True)  # Remove commas
data['Enrollment'] = data['Enrollment'].replace('N/A', '0')  # Replace 'N/A' with '0'
data['Enrollment'] = data['Enrollment'].astype(int)

# Define your generalized categories and associated keywords
category_keywords = {
    'Cancer': [
        'Colon Cancer',
        'Fallopian Tube Cancer',
        'Ovarian Cancer',
        'Abdominal Aortic Aneurysm (AAA)',
        'Prostatic Cancer',
        'Gynecologic Cancer',
        'Breast Neoplasms',
        'Cervical Cancer',
        'Pancreatic Disease',
        'HCC (Hepatocellular Carcinoma)',
        'Neovascular Age-Related Macular Degeneration',
        'Oral Neoplasm',
        'Skin Cancer',
        'Lung Malignancy',
        'Myelofibrosis',
        'Myeloproliferative Neoplasm',
        'Myeloproliferative Disorders',
        'Follicular Lymphoma',
        'Mantle Cell Lymphoma',
        'Marginal Zone Lymphoma',
        'Non Small Cell Lung Cancer',
        'Cholangiocarcinoma',
        'Glioblastoma',
        'Central Nervous System Tumor',
        'Urothelial Carcinoma',
        'Bladder Cancer',
        'Endometrial Cancer',
        'Testicular Cancer',
        'Prostate Carcinoma',
        'Gastrointestinal Neuroendocrine Tumor',
        'Carcinoma',
        'Mismatch Repair Deficiency',
        'BRCA Gene Rearrangement',
        'Non Hodgkin Lymphoma',
        'Leukemia'
    ],
    'Cardiovascular Diseases': [
        'Cardiac Disease',
        'Acute Coronary Syndrome',
        'Coronary Artery Disease',
        'Ischaemic Heart Disease',
        'Hypertension',
        'Heart Failure',
        'Atrial Fibrillation',
        'Arrhythmias, Cardiac',
        'Valvular Heart Disease',
        'Coronary Microvascular Disease'
    ],
    'Neurological Disorders': [
        'Alzheimer Disease',
        'Mild Cognitive Impairment',
        'Dementia With Lewy Bodies',
        'Dementia, Vascular',
        'Frontotemporal Dementia',
        'Primary Progressive Aphasia',
        'Parkinson Disease',
        'Motor Neuron Disease',
        'Major Depressive Disorder',
        'Bipolar Disorder',
        'Amyotrophic Lateral Sclerosis',
        'Stroke',
        'Stroke Rehabilitation',
        'Inflammatory Bowel Diseases',
        'Sleep-Disordered Breathing',
        'Sleep Architecture',
        'Weakness, Muscle',
        'Delirium in Old Age',
        'Muscle Atrophy or Weakness',
        'Muscle Loss',
        'Hospital Acquired Condition',
        'Physical Disability',
        'Physical Inactivity',
        'Dementia',
        'Mild Cognitive Impairment',
        'Normal Cognition',
        'Preclinical Alzheimer\'s Disease',
        'Prodromal Alzheimer\'s Disease',
        "Alzheimer's Disease (Incl Subtypes)"
    ],
    'Infectious Diseases': [
        'COVID',
        'COVID 19',
        'SARS-CoV 2',
        'HIV Infections',
        'Acquired Immunodeficiency Syndrome',
        'Sexually Transmitted Diseases',
        'Viral',
        'Herpes Zoster',
        'Dermatitis, Seborrheic',
        'Pneumonia',
        'Infectious Mononucleosis',
        'Psoriasis',
        'Candida Infection',
        'Lymphadenopathy',
        'Uterine Cervical Dysplasia',
        'Weight Loss',
        'Diarrhea Chronic',
        'Leukopenia',
        'Thrombocytopenia',
        'AIDS Defining Illness',
        'HIV Indicator Condition',
        'Tuberculosis',
        'SARS-CoV Infection'
    ],
    'Gastrointestinal Disorders': [
        'Colonoscopy',
        'Colon Diseases',
        'Colon Lesion',
        'Colon Polyp',
        'Colorectal Polyp',
        'Gastric Diseases',
        'Gastric Intestinal Metaplasia',
        'Gastric Cancer',
        'Colonic Polyp',
        'Gastrointestinal Tract Cancers',
        'Gastrointestinal Disease',
        'Inflammatory Bowel Diseases',
        'Colorectal Neoplasms',
        'Colonic Adenoma',
        'Colonic Adenoma',
        'Colorectal Adenoma',
        'Colorectal Neoplasms',
        'Endoscopic Retrograde Cholangiopancreatography',
        'Pouches, Ileoanal',
        'Pouches',
        'Ileocolic Intussusception',
        'Gastro-Intestinal Disorders',
        'Gastric Cancer',
        'Esophageal Cancer',
        'Esophagogastric Junction Cancer',
        'Polyps',
        'Adenoma Colon',
        'Colon Adenoma',
        'Colorectal Adenomatous'
    ]
}

# Create columns for each category and initialize them with 0
for category in category_keywords:
    data[category] = 0

# Check if keywords are present in the 'Condition' column and set the corresponding category columns to 1
for category, keywords in category_keywords.items():
    for keyword in keywords:
        data[category] = data[category] | data['Condition'].str.contains(keyword, case=False, regex=False)

# Drop the original 'Condition' column
data.drop('Condition', axis=1, inplace=True)

# Categorical data handling for 'Location' using one-hot encoding
location_dummies = pd.get_dummies(data['Location'], prefix='Location')
data = pd.concat([data, location_dummies], axis=1)
data.drop('Location', axis=1, inplace=True)

# Categorical data handling for 'Phase'
data['Phase'] = data['Phase'].str.replace('Unaddressed', '0')
data['Phase'] = data['Phase'].str.replace('Not Applicable', '0')
data['Phase'] = data['Phase'].str.replace('Phase 1', '1')
data['Phase'] = data['Phase'].str.replace('Phase 2', '2')
data['Phase'] = data['Phase'].str.replace('Phase 3', '3')
data['Phase'] = data['Phase'].str.replace('Phase 4', '4')

# Categorical data handling for 'Study Type (Interventional or Observation)
data['Interventional'] = data['Study Type'].apply(lambda x: 1 if x == 'Interventional' else 0)
data['Observational'] = data['Study Type'].apply(lambda x: 1 if x == 'Observational' else 0)

# Drop the original 'Study Type' column
data.drop('Study Type', axis=1, inplace=True)

# Save the cleaned data to a new file
data.to_csv('cleaned_clinical_trials_data_new_2.csv', index=False)
data.to_json('cleaned_clinical_trials_data_new_2.json', orient='records', lines=True)


