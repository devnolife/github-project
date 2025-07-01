from typing import List
from utils.validators import validate_proposal_data


class Proposal:
    def __init__(self, title: str, description: str, conclusions: str):
        self.title = title
        self.description = description
        self.conclusions = conclusions
        self.conclusions_list = self._parse_conclusions(conclusions)

    def _parse_conclusions(self, conclusions: str) -> List[str]:
        """Parse conclusions string into a list of individual conclusions."""
        if not conclusions:
            return []
        # Split by newlines or semicolons and clean up
        items = [item.strip() for item in conclusions.replace(';', '\n').split('\n')]
        return [item for item in items if item]

    def is_valid(self) -> bool:
        """Validate the proposal data."""
        try:
            validate_proposal_data(self.title, self.description, self.conclusions_list)
            return True
        except ValueError:
            return False

    def format_proposal(self) -> str:
        """Format the proposal for display."""
        formatted = f"Title: {self.title}\n\nDescription: {self.description}\n\nConclusions:\n"
        for conclusion in self.conclusions_list:
            formatted += f"- {conclusion}\n"
        return formatted.strip()

    def to_dict(self) -> dict:
        """Convert proposal to dictionary."""
        return {
            'title': self.title,
            'description': self.description,
            'conclusions': self.conclusions_list
        }
