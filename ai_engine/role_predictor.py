"""Baseline role predictor: TF-IDF + LogisticRegression.

Provides a small, trainable predictor with CSV-loading convenience and
model persistence to avoid retraining on every startup. Falls back to a
keyword-based scorer when no trained model is available.
"""
import os
import csv
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    import numpy as np
    _SKLEARN_AVAILABLE = True
except Exception:
    TfidfVectorizer = None
    LogisticRegression = None
    np = None
    _SKLEARN_AVAILABLE = False

try:
    import joblib
    _JOBLIB_AVAILABLE = True
except Exception:
    joblib = None
    _JOBLIB_AVAILABLE = False

MODEL_DIR = os.getenv('MODEL_DIR', 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'role_predictor.joblib')


class RolePredictor:
    def __init__(self):
        self.vectorizer = None
        self.model = None
        self.trained = False

    def train(self, texts: List[str], labels: List[str]) -> bool:
        if not _SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn is required for training RolePredictor")
        if not texts or not labels or len(texts) != len(labels):
            return False

        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english', max_features=5000)
        X = self.vectorizer.fit_transform(texts)
        clf = LogisticRegression(max_iter=1000)
        clf.fit(X, labels)
        self.model = clf
        self.trained = True
        return True

    def train_from_csv(self, csv_path: str = "data/training_dataset.csv") -> bool:
        if not os.path.exists(csv_path):
            return False
        texts = []
        labels = []
        try:
            with open(csv_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    t = row.get('text') or row.get('resume') or row.get('description')
                    l = row.get('role') or row.get('label')
                    if t and l:
                        texts.append(t)
                        labels.append(l)
        except Exception:
            logger.exception("Failed to read training CSV")
            return False

        if texts and labels:
            ok = self.train(texts, labels)
            return ok
        return False

    def predict(self, text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Return top_k role predictions with scores.

        If the model is not trained, use a keyword-based fallback.
        """
        if not text:
            return []

        if self.trained and self.vectorizer is not None and self.model is not None:
            X = self.vectorizer.transform([text])
            probs = self.model.predict_proba(X)[0]
            classes = list(self.model.classes_)
            # sort by probability descending
            if _SKLEARN_AVAILABLE and np is not None:
                idx = list(reversed(list(np.argsort(probs))))[:top_k]
            else:
                idx = sorted(range(len(probs)), key=lambda i: probs[i], reverse=True)[:top_k]
            return [{'role': classes[i], 'score': float(probs[i])} for i in idx]

        # Fallback: simple keyword scoring
        lower = text.lower()
        mapping = {
            'Data Scientist': ['data', 'machine learning', 'model', 'pandas', 'numpy', 'scikit-learn', 'ml'],
            'Web Developer': ['javascript', 'react', 'frontend', 'backend', 'node.js', 'express', 'html', 'css'],
            'DevOps Engineer': ['docker', 'kubernetes', 'ci/cd', 'jenkins', 'terraform', 'aws', 'gcp', 'azure'],
            'Android Developer': ['android', 'kotlin', 'java', 'android studio'],
            'Machine Learning Engineer': ['deep learning', 'tensorflow', 'pytorch', 'neural network'],
            'Backend Developer': ['api', 'rest', 'django', 'flask', 'spring', 'sql', 'postgresql', 'mysql'],
            'Frontend Developer': ['react', 'vue', 'angular', 'typescript', 'css', 'html']
        }
        scores = []
        for role, keywords in mapping.items():
            score = sum(1 for kw in keywords if kw in lower) / max(1, len(keywords))
            scores.append((role, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return [{'role': r, 'score': float(s)} for r, s in scores[:top_k]]

    def save_model(self, path: str = MODEL_PATH) -> bool:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            data = {
                'vectorizer': self.vectorizer,
                'model': self.model
            }
            if _JOBLIB_AVAILABLE:
                joblib.dump(data, path)
            else:
                import pickle
                with open(path, 'wb') as f:
                    pickle.dump(data, f)
            return True
        except Exception:
            logger.exception("Failed to save role predictor model")
            return False

    def load_model(self, path: str = MODEL_PATH) -> bool:
        if not os.path.exists(path):
            return False
        try:
            if _JOBLIB_AVAILABLE:
                data = joblib.load(path)
            else:
                import pickle
                with open(path, 'rb') as f:
                    data = pickle.load(f)
            self.vectorizer = data.get('vectorizer')
            self.model = data.get('model')
            self.trained = bool(self.vectorizer and self.model)
            return self.trained
        except Exception:
            logger.exception("Failed to load role predictor model")
            return False


# Singleton instance
role_predictor = RolePredictor()
# Try to load persisted model, otherwise train from bundled CSV if available
try:
    loaded = role_predictor.load_model()
    if not loaded:
        role_predictor.train_from_csv('data/training_dataset.csv')
        # Save the newly trained model if training succeeded
        try:
            role_predictor.save_model()
        except Exception:
            pass
except Exception:
    # Silent failure; predictor will use fallback
    pass
