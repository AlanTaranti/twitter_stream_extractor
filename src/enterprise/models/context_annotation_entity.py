class ContextAnnotationEntity:
    def __init__(self, data):
        self.id: int = data.get("id", None)
        self.name: str = data.get("name", None)
        self.description: str = data.get("description", None)
