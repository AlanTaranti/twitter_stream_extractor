from src.enterprise.models.context_annotation_domain import ContextAnnotationDomain
from src.enterprise.models.context_annotation_entity import ContextAnnotationEntity


class ContextAnnotation:
    def __init__(self, data):
        self.domain: ContextAnnotationDomain = ContextAnnotationDomain(
            data.get("domain", {})
        )
        self.entity: ContextAnnotationEntity = ContextAnnotationEntity(
            data.get("entity", {})
        )
