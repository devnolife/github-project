from typing import Optional, Dict, Any
from datetime import datetime


class GitHubProject:
    def __init__(self, name: str, full_name: str = None, html_url: str = None, 
                 description: str = None, language: str = None, 
                 stargazers_count: int = 0, forks_count: int = 0,
                 open_issues_count: int = 0, created_at: str = None,
                 updated_at: str = None, **kwargs):
        self.name = name
        self.full_name = full_name or name
        self.html_url = html_url
        self.description = description or "No description available"
        self.language = language
        self.stargazers_count = stargazers_count
        self.forks_count = forks_count
        self.open_issues_count = open_issues_count
        self.created_at = created_at
        self.updated_at = updated_at
        
        # Store any additional data
        self.additional_data = kwargs

    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> 'GitHubProject':
        """Create GitHubProject instance from GitHub API response."""
        return cls(**api_data)

    def get_project_stats(self) -> str:
        """Get formatted project statistics."""
        stats = []
        if self.language:
            stats.append(f"Language: {self.language}")
        stats.append(f"Stars: {self.stargazers_count}")
        stats.append(f"Forks: {self.forks_count}")
        stats.append(f"Open Issues: {self.open_issues_count}")
        return " | ".join(stats)

    def get_formatted_date(self, date_str: str) -> str:
        """Format ISO date string to readable format."""
        if not date_str:
            return "Unknown"
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime("%B %d, %Y")
        except:
            return date_str

    def __str__(self):
        return (f"Project: {self.full_name}\n"
                f"URL: {self.html_url}\n"
                f"Description: {self.description}\n"
                f"Stats: {self.get_project_stats()}\n"
                f"Created: {self.get_formatted_date(self.created_at)}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'name': self.name,
            'full_name': self.full_name,
            'html_url': self.html_url,
            'description': self.description,
            'language': self.language,
            'stargazers_count': self.stargazers_count,
            'forks_count': self.forks_count,
            'open_issues_count': self.open_issues_count,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
