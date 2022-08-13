from enterprise.models.context_annotation_domain import ContextAnnotationDomain
from enterprise.models.context_annotation_entity import ContextAnnotationEntity


class ContextAnnotation:
    def __init__(self, data):
        self.domain: ContextAnnotationDomain = ContextAnnotationDomain(data["domain"])
        self.entity: ContextAnnotationEntity = ContextAnnotationEntity(data["entity"])