from typing import Any, Dict, List, Optional, Text, Tuple, Type, Callable
from vma_nlu.ner.extractor import Extractor

from rasa.nlu.components import Component
from rasa.nlu.extractors.extractor import EntityExtractor
from rasa.nlu.config import RasaNLUModelConfig
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.training_data.message import Message


class PatternExtractor(EntityExtractor):
    name = "PatternExtractor"
    defaults = {
        "n_gram": 4,
        "load_dict": False,
        "mode": "pattern",
    }

    def __init__(
        self,
        component_config: Optional[Dict[Text, Any]] = None,
    ) -> None:
        super(PatternExtractor, self).__init__(component_config)

        self.extractor = Extractor(self.component_config["n_gram"], self.component_config["load_dict"])

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
        intent = message.data.get('intent')
        if text:
            output = self.extractor.extract_ner(text, intent['name'])
            old_entities = message.data.get("entities")
            for entity in output:
                entity['extractor'] = 'PatternExtractor'
                if entity['entity'] == 'time' and entity["value"]:
                    entity['value'] = f'{entity["value"][0]}:{entity["value"][1]}'
                    old_entities.append(entity)
                elif entity['entity'] == 'date_time' and entity["value"]:
                    first_date_extracted = entity["value"][0]
                    if first_date_extracted[1] and first_date_extracted[2] and first_date_extracted[3]:
                        entity['value'] = f'{first_date_extracted[1]}/{first_date_extracted[2]}/{first_date_extracted[3]}'
                        old_entities.append(entity)
                    elif first_date_extracted[2] and first_date_extracted[3]:
                        entity['value'] = f'xx/{first_date_extracted[2]}/{first_date_extracted[3]}'
                        old_entities.append(entity)
                    elif first_date_extracted[3]:
                        entity['value'] = f'xx/xx/{first_date_extracted[3]}'
                        old_entities.append(entity)
                else:
                    old_entities.append(entity)
            message.set("entities", old_entities, add_to_output=True)
        

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

        if cached_component:
            return cached_component
        else:
            return cls(meta)
