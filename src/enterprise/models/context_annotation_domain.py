class ContextAnnotationDomain:
    def __init__(self, data):
        self.id: int = data["id"]
        self.name: str = data["name"]
        self.description = data["description"]
