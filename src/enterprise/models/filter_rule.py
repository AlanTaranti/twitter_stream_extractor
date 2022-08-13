class FilterRule:
    def __init__(self, data):
        self.id: int = data.get("id", None)
        self.value: str = data.get("value", None)
        self.tag: str = data.get("tag", None)

    def __str__(self):
        return f"{self.id} - {self.value} - {self.tag}"

    def __repr__(self):
        return self.__str__()
