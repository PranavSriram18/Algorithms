from collections import Counter, defaultdict
from functools import reduce
from typing import List, Dict, Optional


class Attendees:
    def __init__(self, data: List[Dict]):
        self.data = data
        self.n = len(self.data)
        self.build_e2a()

    def get_average_age(self) -> float:
        return sum(p['age'] for p in self.data) / self.n

    def find_most_popular_event(self) -> Optional[str]:
        c = Counter()
        c.update(event for entry in self.data for event in entry['events'])
        return c.most_common(1)[0][0] if c else None
    
    def build_e2a(self) -> None:
        self.e2a = defaultdict(list)
        for entry in self.data:
            for event in entry['events']:
                self.e2a[event].append(entry['name'])
    
    def get_attendees_for_event(self, event: str) -> List[str]:
        return self.e2a.get(event, [])
    
    def has_attended_all_events(self, events: List[str]) -> bool:
        def attended_all(entry, events):
            return all(event in entry['events'] for event in events)
        return any(attended_all(entry, events) for entry in self.data)
    
    def sort_attendees_by_events(self):
        



if __name__=="__main__":
    attendees = [
        {"name": "Alice", "age": 25, "events": ["Python Workshop", "Data Science Seminar", "AI Conference"]},
        {"name": "Bob", "age": 30, "events": ["Java Meetup", "Cloud Computing Talk"]},
        {"name": "Charlie", "age": 35, "events": ["Python Workshop", "Agile Methodology", "Cloud Computing Talk"]},
        {"name": "David", "age": 28, "events": ["Data Science Seminar", "AI Conference", "Machine Learning Bootcamp"]},
        {"name": "Eve", "age": 22, "events": ["Python Workshop", "Web Development 101"]}
]