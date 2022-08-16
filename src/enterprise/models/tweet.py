from typing import List

from enterprise.models.context_annotation import ContextAnnotation


class Tweet:
    def __init__(self, data):
        self.id: int = data.get("id", None)
        self.text: str = data.get("text", None)
        self.context_annotations: List[ContextAnnotation] = [
            ContextAnnotation(annotation)
            for annotation in data.get("context_annotations", [])
        ]
        self.lang: str = data.get("lang", None)

    def __str__(self):
        return f"{self.id} - {self.text}"

    def __repr__(self):
        return self.__str__()
