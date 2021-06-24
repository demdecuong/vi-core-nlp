import os
import pickle
import logging
import re
import numpy as np
from typing import Any, Dict, List, Optional, Text, Tuple, Type

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from rasa.nlu.components import Component
from rasa.nlu.classifiers.classifier import IntentClassifier
from rasa.shared.nlu.constants import INTENT, TEXT
from rasa.nlu.config import RasaNLUModelConfig
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.training_data.message import Message

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(WORK_DIR, "weight/LR_model.pkl")

logger = logging.getLogger(__name__)


class LogisticRegressionClassifier(IntentClassifier):
    name = "LogisticRegressionClassifier"

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None, learner=None) -> None:
        super(LogisticRegressionClassifier, self).__init__(component_config)
        self.learner = learner

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        """Train LR classifier"""
        X_train = [e.get(TEXT) for e in training_data.intent_examples]
        y_train = [e.get(INTENT) for e in training_data.intent_examples]

        X_train, X_test, y_train, y_test = train_test_split(
            X_train, y_train, test_size=0.2, random_state=42)
        text_clf = Pipeline([('vect', CountVectorizer(ngram_range=(1, 2),
                                                      max_df=0.8,
                                                      max_features=None)),

                             ('clf', SGDClassifier(loss='log'))
                             ])
        self.learner = text_clf.fit(X_train, y_train)

    def process(self, message: Message, **kwargs: Any) -> None:
        """Process an incoming message."""

        if not self.learner:
            intent = None
            intent_ranking = []
        else:
            text = message.data.get('text')
            output = self.predict(text)
            intent = output.get("intent")
            intent_ranking = output.get("intent_ranking")

        message.set("intent", intent, add_to_output=True)
        message.set("intent_ranking", intent_ranking, add_to_output=True)

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this component to disk for future loading."""
        classifier_file_name = file_name + "_classifier.pkl"
        pickle.dump(self.learner, open(os.path.join(model_dir, classifier_file_name), "wb"))

        return {"classifier": classifier_file_name}

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Text,
        model_metadata: Optional["Metadata"] = None,
        cached_component: Optional["Component"] = None,
        **kwargs: Any,
    ) -> "Component":
        """Load this component from file."""
        classifier_file = os.path.join(model_dir, meta.get("classifier"))
        if not os.path.isfile(classifier_file):
            logger.error(
                f"File not found. Cannot load LR model: {classifier_file}")
            return cls(component_config=meta)
        else:
            try:
                learner = pickle.load(open(classifier_file, 'rb'))
                logger.debug(f"Loads LR model successfully ")
                return cls(meta, learner)
            except Exception as ex:
                logger.error(
                    f"Cannot load LR model: {classifier_file}: error: {ex}")

    def predict(self, text: Text):
        text = [self.normalize_text(text)]
        predict = self.learner.predict(text)
        confidence = np.max(self.learner.predict_proba(text)[0])
        return {
            "intent": {
                "name": predict[0],
                "confidence": confidence
            },
            "intent_ranking": []
        }

    def normalize_text(self, s):
        s = re.sub(r'([a-z])\1+', lambda m: m.group(1), s, flags=re.IGNORECASE)
        s = re.sub(r'([a-z][a-z])\1+', lambda m: m.group(1), s, flags=re.IGNORECASE)
        return s