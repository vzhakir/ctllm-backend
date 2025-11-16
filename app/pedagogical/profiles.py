class UserProfile:
    def __init__(self, name: str, occupation: str, age: int, learning_type: str, ct_focus: str):
        self.name = name
        self.occupation = occupation
        self.age = age
        self.learning_type = learning_type   # TAR / PAI / GR
        self.ct_focus = ct_focus             # Algorithmic / Spatial / Linguistic etc.