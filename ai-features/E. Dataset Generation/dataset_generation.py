"""Dataset generation utilities — migrated into a numbered directory

This file contains helper lists and simple dataset generation utilities. It
was moved from datasetGeneration.py into a dedicated folder to match the
`N. Feature Name` structure used across the codebase.
"""

import random
import itertools
import re
import json
import time

# --- sample lists (trimmed for brevity in the migration) ---
degrees = [
    "BSc", "MSc", "PhD", "Diploma", "MBA", "BEng", "MEng", "BS", "MS",
    "DEng", "DPhil", "Associate's Degree", "Professional Certificate",
    "Bachelor of Science", "Master of Science", "Doctor of Philosophy"
]

majors = [
    "Computer Science", "Artificial Intelligence", "Data Science",
    "Software Engineering", "Cybersecurity", "Information Systems"
]

universities = [
    "Cairo University", "Ain Shams University", "MIT", "Stanford University",
    "Alexandria University", "Helwan University"
]

roles = [
    "Software Engineer", "Data Scientist", "ML Engineer", "Backend Developer",
    "Frontend Developer", "Cloud Architect"
]

companies = ["Vodafone", "Microsoft", "IBM", "Google", "Amazon", "Meta"]

techs = ["Python", "TensorFlow", "PyTorch", "Flask", "React", "AWS", "Docker"]

projects = ["chatbot", "recommendation engine", "image segmentation model", "fraud detection system"]

skills = ["machine learning", "deep learning", "computer vision", "NLP", "data visualization"]

certs = ["AWS Certified Machine Learning - Specialty", "Google Cloud Professional Cloud Architect"]


def random_profile(seed: int = None) -> dict:
    rng = random.Random(seed)
    return {
        "name": rng.choice(["Alex","Sam","Jordan","Taylor"]),
        "education": rng.choice(universities),
        "degree": rng.choice(degrees),
        "major": rng.choice(majors),
        "skills": rng.sample(skills, k=min(3, len(skills)))
    }


if __name__ == "__main__":
    for i in range(5):
        print(random_profile(i))
