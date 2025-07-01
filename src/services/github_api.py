import requests
from typing import Dict, Any, Optional
from config.settings import GITHUB_API_URL, API_KEY


class GitHubAPIError(Exception):
    """Custom exception for GitHub API errors."""
    pass


class GitHubAPI:
    def __init__(self, base_url: str = GITHUB_API_URL, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key or API_KEY
        self.session = requests.Session()
        
        # Set up authentication if API key is provided
        if self.api_key and self.api_key != "your_api_key_here":
            self.session.headers.update({
                'Authorization': f'token {self.api_key}',
                'Accept': 'application/vnd.github.v3+json'
            })

    def fetch_project_data(self, project_name: str) -> Dict[str, Any]:
        """
        Fetch project data from GitHub API.
        
        Args:
            project_name: Repository name in format 'owner/repo'
            
        Returns:
            Dictionary containing project data
            
        Raises:
            GitHubAPIError: If API request fails
        """
        if '/' not in project_name:
            raise GitHubAPIError(f"Invalid project name format: '{project_name}'. Expected 'owner/repo'")
        
        url = f"{self.base_url}/repos/{project_name}"
        
        try:
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                raise GitHubAPIError(f"Repository '{project_name}' not found")
            elif response.status_code == 403:
                raise GitHubAPIError("API rate limit exceeded or access forbidden")
            else:
                raise GitHubAPIError(f"GitHub API request failed with status {response.status_code}: {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise GitHubAPIError(f"Network error while fetching project data: {str(e)}")

    def fetch_repository_readme(self, project_name: str) -> Optional[str]:
        """
        Fetch repository README content.
        
        Args:
            project_name: Repository name in format 'owner/repo'
            
        Returns:
            README content as string or None if not found
        """
        url = f"{self.base_url}/repos/{project_name}/readme"
        
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                # Decode base64 content
                import base64
                content = base64.b64decode(data['content']).decode('utf-8')
                return content
            return None
        except Exception:
            return None

    def validate_repository_exists(self, project_name: str) -> bool:
        """
        Check if a repository exists.
        
        Args:
            project_name: Repository name in format 'owner/repo'
            
        Returns:
            True if repository exists, False otherwise
        """
        try:
            self.fetch_project_data(project_name)
            return True
        except GitHubAPIError:
            return False
