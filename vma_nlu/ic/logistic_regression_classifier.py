import os
import pickle
import logging
import numpy as np
from typing import Any, Dict, List, Optional, Text, Tuple, Type

from rasa.nlu.components import Component
from rasa.nlu.classifiers.classifier import IntentClassifier
from rasa.nlu.config import RasaNLUModelConfig
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.training_data.message import Message

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(WORK_DIR, "weight/LR_model.pkl")

logger = logging.getLogger(__name__)

class LogisticRegressionClassifier(IntentClassifier):
    name = "LogisticRegressionClassifier"

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None, learner = None) -> None:
        super(LogisticRegressionClassifier, self).__init__(component_config)
        self.learner = learner

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        """Train this component.

        This is the components chance to train itself provided
        with the training data. The component can rely on
        any context attribute to be present, that gets created
        by a call to :meth:`components.Component.pipeline_init`
        of ANY component and
        on any context attributes created by a call to
        :meth:`components.Component.train`
        of components previous to this one."""
        pass

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

        pass

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

        if not os.path.isfile(MODEL_PATH):
            logger.error(f"File not found. Cannot load Naive Bayes model: {MODEL_PATH}")
            return cls(component_config=meta)
        else:
            try:
                learner = pickle.load(open(MODEL_PATH, 'rb'))
                logger.debug(f"Load {{self.__class__.__name__}} Naive Bayes model successfully ")
                return cls(meta, learner)
            except Exception as ex:
                logger.error(f"Cannot load Naive Bayes model: {MODEL_PATH}: error: {ex}")

    def predict(self, text: Text):
        text = [text]
        predict = self.learner.predict(text)
        confidence = np.max(self.learner.predict_proba(text)[0])
        return {
            "intent":{
                "name":predict[0],
                "confidence": confidence
            },
            "intent_ranking":[]
        }