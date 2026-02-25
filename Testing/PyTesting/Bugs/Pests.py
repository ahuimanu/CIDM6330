class Pest:
    def __init__(self):
        self.species = None


class PestObservation:
    def __init__(self):
        self.city = None
        self.county = None
        self.obs_date = None


class MaladyType:
    def __init__(self):
        self.known_vectors: Pest = []


class ImpactObservation:
    def __init__(self):
        self.malady_type = None
        self.species = None
        self.city = None
        self.county = None
        self.obs_date = None
