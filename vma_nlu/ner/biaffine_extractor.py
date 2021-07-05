import os
import logging
from typing import Any, Dict, List, Optional, Text, Tuple, Type, Callable
from vma_nlu.ner.extractor import Extractor

from rasa.nlu.components import Component
from rasa.nlu.extractors.extractor import EntityExtractor
from rasa.nlu.config import RasaNLUModelConfig
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.training_data.message import Message
from vma_nlu.ner.pername_deeplearning.inference import Inference

logger = logging.getLogger(__name__)

class BiaffineExtractor(EntityExtractor):
    name = "BiaffineExtractor"

    defaults = {
        "label_set_path": "",
        "char_vocab_path": "",
        "checkpoint": "",
    }

    def __init__(
        self,
        component_config: Optional[Dict[Text, Any]] = None,
        learner = None,
    ) -> None:
        super(BiaffineExtractor, self).__init__(component_config)
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
        text = message.data.get('text')
        if text:
            result = self.learner.inference(text)
            old_entities = message.data.get("entities")
            for e in result.get("entities"):
                e["extractor"] = "BiaffineExtractor"
                e["value"] = e["value"].title()
                old_entities.append(e)
            message.set("entities", old_entities, add_to_output=True)
        

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this component to disk for future loading."""

        label_set_path = self.component_config.get("label_set_path")
        char_vocab_path = self.component_config.get("char_vocab_path")
        checkpoint = self.component_config.get("checkpoint")

        return {"label_set_path": label_set_path, "char_vocab_path": char_vocab_path, "checkpoint": checkpoint}

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
        label_set_path = meta.get("label_set_path")
        char_vocab_path = meta.get("char_vocab_path")
        checkpoint = meta.get("checkpoint")
        if not os.path.isfile(label_set_path) or not os.path.isfile(char_vocab_path) or not os.path.isfile(checkpoint):
            logger.error(f"File not found. Cannot load Biaffine Extractor model: {checkpoint}")
            return cls(component_config=meta)
        else:
            try:
                learner = Inference(label_set_path, char_vocab_path, checkpoint)
                logger.debug(f"Load Biaffine Extractor model successfully ")
                return cls(meta, learner)
            except Exception as ex:
                logger.error(f"Cannot load Biaffine Extractor model: {checkpoint}: error: {ex}")
