import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, pipeline
from transformers import AutoTokenizer
from typing import List, Dict


def extract_experience_items(resume):
        experience_items = [exp['description'] for exp in resume.get('experienceItem', [])]
        return ' '.join(experience_items).replace(' ,', ',').replace(' .', '.')




class NERModel:
    def __init__(self, model_folder: str):
        self.model = pipeline("ner", model=model_folder, aggregation_strategy="max")

    def __call__(self, text: str) -> List[Dict]:
        return self.model(text)
    
    
class EmbeddingMatcher:
    def __init__(self):
        self.model = SentenceTransformer("intfloat/multilingual-e5-large")


    def encode_text(self, text):

        return self.model.encode(text)
    
    

    def calculate_similarity(self, embeddings1, embeddings2):

        return cosine_similarity([embeddings1], [embeddings2])


def main(resumes, vacancy, model_path):
    ner_model = NERModel(model_path)
    extracted_resumes = [ner_model(resume) for resume in resumes]
    normilized_resumes = [extract_experience_items(resume) for resume in extracted_resumes]
    

    matcher = EmbeddingMatcher()
    embeddings_resumes = matcher.encode_text(normilized_resumes)
    embeddings_vacancy = matcher.encode_text(vacancy)
    scores = []
    for i in range(len(embeddings_resumes)):
        scores.append(matcher.calculate_similarity(embeddings_vacancy, embeddings_resumes[i]))
    
    return scores