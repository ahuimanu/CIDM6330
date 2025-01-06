import uuid
from datetime import datetime


class Competency:
    def __init__(self, name, description="", level="low", knowledgeskillpair=None):
        self.id = uuid.uuid4()
        self.name = name
        self.description = description
        self.level = level
        self.knowledgeskillpair = knowledgeskillpair
        # Metadata fields
        self.created_timestamp = datetime.now()
        self.updated_timestamp = datetime.now()
