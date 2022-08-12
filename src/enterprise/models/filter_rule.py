class FilterRule:
    def __init__(self, data):
        self.id: int = data["id"]
        self.value: str = data["value"]
        self.tag = data["tag"]
