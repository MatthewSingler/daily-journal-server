class Entry():
    def __init__(self, id, concept, text, date, mood_id):
        self.id = id
        self.concept = concept
        self.text = text
        self.date = date
        self.mood_id = mood_id
        self.mood = None