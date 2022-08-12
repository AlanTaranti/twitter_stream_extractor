from typing import List

from enterprise.models.context_annotation import ContextAnnotation


class Tweet:
    def __init__(self, data):
        self.id = data["id"]
        self.text = data["text"]
        self.context_annotations: List[ContextAnnotation] = [
            ContextAnnotation(annotation) for annotation in data["context_annotations"]
        ]
        self.lang: str = data["lang"]
