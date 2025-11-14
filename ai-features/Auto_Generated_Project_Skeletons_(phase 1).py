import os
import json
from datetime import datetime

# -----------------------------------------
# FEATURE 12: Auto-Generated Project Skeletons
# -----------------------------------------

class ProjectSkeletonGenerator:

    def __init__(self, base_output_dir="generated_projects"):
        self.base_output_dir = base_output_dir
        os.makedirs(self.base_output_dir, exist_ok=True)

        # === Skill → Project Templates ===
        self.skill_templates = {
            "machine learning": self._ml_project_template,
            "nlp": self._nlp_project_template,
            "data analysis": self._data_analysis_template,
            "deep learning": self._dl_project_template,
            "computer vision": self._cv_project_template
        }

    # -----------------------------------------
    # Public API
    # -----------------------------------------

    def generate_project(self, missing_skill: str):
        """
        Generate a code+folder project skeleton based on a missing skill.
        """
        skill = missing_skill.lower()

        if skill not in self.skill_templates:
            return {
                "status": "error",
                "message": f"No template available for skill: {missing_skill}"
            }

        # Generate unique project folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = os.path.join(self.base_output_dir, f"{skill.replace(' ', '_')}_{timestamp}")
        os.makedirs(project_dir, exist_ok=True)

        # Generate project files
        template_fn = self.skill_templates[skill]
        template_data = template_fn()

        self._create_files(project_dir, template_data)

        return {
            "status": "success",
            "project_path": project_dir,
            "files_created": list(template_data.keys())
        }

    # -----------------------------------------
    # Internal: Create files
    # -----------------------------------------

    def _create_files(self, project_dir, template_data):
        for filename, content in template_data.items():
            filepath = os.path.join(project_dir, filename)
            folder = os.path.dirname(filepath)
            os.makedirs(folder, exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

    # -----------------------------------------
    # Template Factories
    # -----------------------------------------

    def _ml_project_template(self):
        return {
            "README.md": self._readme("Machine Learning Classification Project"),
            "src/model.py": self._ml_model_code(),
            "src/dataset_loader.py": self._dataset_loader_code(),
            "src/train.py": self._ml_train_code(),
            "requirements.txt": "pandas\nscikit-learn\nnumpy\nmatplotlib\n"
        }

    def _nlp_project_template(self):
        return {
            "README.md": self._readme("NLP Text Classification Project"),
            "src/text_preprocessing.py": self._text_preprocess_code(),
            "src/model.py": self._nlp_model_code(),
            "src/train.py": self._nlp_train_code(),
            "requirements.txt": "pandas\nscikit-learn\nnumpy\nnltk\n"
        }

    def _data_analysis_template(self):
        return {
            "README.md": self._readme("Data Analysis Exploratory Project"),
            "notebooks/EDA.ipynb": "",
            "requirements.txt": "pandas\nnumpy\nmatplotlib\nseaborn\n"
        }

    def _dl_project_template(self):
        return {
            "README.md": self._readme("Deep Learning Image Classifier"),
            "src/model.py": self._dl_model_code(),
            "src/train.py": self._dl_train_code(),
            "requirements.txt": "torch\ntorchvision\nnumpy\n"
        }

    def _cv_project_template(self):
        return {
            "README.md": self._readme("Computer Vision Detection Project"),
            "src/detect.py": self._cv_detect_code(),
            "requirements.txt": "opencv-python\nnumpy\n"
        }

    # -----------------------------------------
    # Template Code Snippets
    # -----------------------------------------

    def _readme(self, title):
        return f"# {title}\n\nGenerated automatically by CareerMatch-AI (Feature 12)."

    def _ml_model_code(self):
        return """from sklearn.ensemble import RandomForestClassifier

class MLModel:
    def __init__(self):
        self.model = RandomForestClassifier()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)
"""

    def _dataset_loader_code(self):
        return """import pandas as pd

def load_dataset(path):
    return pd.read_csv(path)
"""

    def _ml_train_code(self):
        return """from dataset_loader import load_dataset
from model import MLModel

data = load_dataset("data.csv")
# TODO: prepare X, y

model = MLModel()
model.train(X, y)
"""

    def _text_preprocess_code(self):
        return """import nltk
from nltk.tokenize import word_tokenize

def preprocess(text):
    return word_tokenize(text.lower())
"""

    def _nlp_model_code(self):
        return """from sklearn.linear_model import LogisticRegression

class NLPModel:
    def __init__(self):
        self.clf = LogisticRegression()

    def train(self, X, y):
        self.clf.fit(X, y)

    def predict(self, X):
        return self.clf.predict(X)
"""

    def _nlp_train_code(self):
        return """from model import NLPModel

print("Train NLP model...")
"""

    def _dl_model_code(self):
        return """import torch.nn as nn

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 16, 3),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(26*26*16, 10)
        )

    def forward(self, x):
        return self.net(x)
"""

    def _dl_train_code(self):
        return """print("Train Deep Learning model...")"""

    def _cv_detect_code(self):
        return """import cv2

def detect(image_path):
    img = cv2.imread(image_path)
    # TODO: Add detection logic
    return img
"""

# -----------------------------------------
# Quick test
# -----------------------------------------

if __name__ == "__main__":
    gen = ProjectSkeletonGenerator()
    print(gen.generate_project("machine learning"))
