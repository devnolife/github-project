import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.github_api import GitHubAPI, GitHubAPIError
from services.proposal_generator import ProposalGenerator
from models.proposal import Proposal
from models.github_project import GitHubProject


class TestGitHubAPI(unittest.TestCase):
    
    def setUp(self):
        self.github_api = GitHubAPI()

    def test_github_api_initialization(self):
        """Test GitHub API initialization."""
        api = GitHubAPI()
        self.assertEqual(api.base_url, 'https://api.github.com')
        self.assertIsNotNone(api.session)

    def test_invalid_repo_name_format(self):
        """Test validation of repository name format."""
        with self.assertRaises(GitHubAPIError):
            self.github_api.fetch_project_data('invalid-format')
    
    @patch('services.github_api.requests.Session.get')
    def test_fetch_project_data_success(self, mock_get):
        """Test successful project data fetching."""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'test-repo',
            'full_name': 'user/test-repo',
            'html_url': 'https://github.com/user/test-repo',
            'description': 'Test repository',
            'language': 'Python',
            'stargazers_count': 100,
            'forks_count': 20
        }
        mock_get.return_value = mock_response
        
        project_data = self.github_api.fetch_project_data('user/test-repo')
        
        self.assertEqual(project_data['name'], 'test-repo')
        self.assertEqual(project_data['language'], 'Python')
        mock_get.assert_called_once()

    @patch('services.github_api.requests.Session.get')
    def test_fetch_project_data_not_found(self, mock_get):
        """Test handling of 404 error."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with self.assertRaises(GitHubAPIError) as context:
            self.github_api.fetch_project_data('user/nonexistent-repo')
        
        self.assertIn('not found', str(context.exception))

    @patch('services.github_api.requests.Session.get')
    def test_fetch_project_data_rate_limit(self, mock_get):
        """Test handling of rate limit error."""
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_get.return_value = mock_response
        
        with self.assertRaises(GitHubAPIError) as context:
            self.github_api.fetch_project_data('user/test-repo')
        
        self.assertIn('rate limit', str(context.exception))

    def test_validate_repository_exists_invalid_format(self):
        """Test repository validation with invalid format."""
        result = self.github_api.validate_repository_exists('invalid-format')
        self.assertFalse(result)


class TestProposalGenerator(unittest.TestCase):
    
    def setUp(self):
        self.proposal_generator = ProposalGenerator()
        self.sample_proposal = Proposal(
            title="Test Proposal",
            description="This is a test proposal for validation purposes.",
            conclusions="Improve documentation\nAdd unit tests\nEnhance user experience"
        )
        self.sample_project = GitHubProject(
            name="test-repo",
            full_name="user/test-repo",
            html_url="https://github.com/user/test-repo",
            description="A test repository",
            language="Python",
            stargazers_count=150,
            forks_count=30,
            open_issues_count=5,
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-12-01T00:00:00Z"
        )

    def test_proposal_generator_initialization(self):
        """Test proposal generator initialization."""
        generator = ProposalGenerator()
        self.assertEqual(len(generator.proposals), 0)

    def test_generate_proposal(self):
        """Test comprehensive proposal generation."""
        result = self.proposal_generator.generate(self.sample_proposal, self.sample_project)
        
        self.assertIsInstance(result, str)
        self.assertIn("Test Proposal", result)
        self.assertIn("user/test-repo", result)
        self.assertIn("Python", result)
        self.assertIn("150", result)  # Stars count
        self.assertIn("Improve documentation", result)
        self.assertIn("Add unit tests", result)

    def test_proposal_storage(self):
        """Test that proposals are stored after generation."""
        initial_count = len(self.proposal_generator.proposals)
        
        self.proposal_generator.generate(self.sample_proposal, self.sample_project)
        
        self.assertEqual(len(self.proposal_generator.proposals), initial_count + 1)
        
        latest = self.proposal_generator.get_latest_proposal()
        self.assertIsNotNone(latest)
        self.assertEqual(latest['user_proposal']['title'], "Test Proposal")

    def test_legacy_methods(self):
        """Test legacy proposal methods for backward compatibility."""
        proposal_data = self.proposal_generator.add_proposal(
            "Legacy Title",
            "Legacy description", 
            ["Legacy conclusion 1", "Legacy conclusion 2"]
        )
        
        self.assertEqual(proposal_data['title'], "Legacy Title")
        self.assertIn('created_at', proposal_data)
        
        formatted = self.proposal_generator.format_proposal(proposal_data)
        self.assertIn("Legacy Title", formatted)
        self.assertIn("Legacy conclusion 1", formatted)

    def test_export_to_markdown(self):
        """Test exporting proposal to markdown."""
        self.proposal_generator.generate(self.sample_proposal, self.sample_project)
        
        markdown = self.proposal_generator.export_proposal_to_markdown()
        self.assertIsInstance(markdown, str)
        self.assertIn("# Test Proposal", markdown)

    def test_get_all_proposals(self):
        """Test retrieving all proposals."""
        # Generate multiple proposals
        self.proposal_generator.generate(self.sample_proposal, self.sample_project)
        
        proposal2 = Proposal("Second Proposal", "Second description", "Second conclusion")
        self.proposal_generator.generate(proposal2, self.sample_project)
        
        all_proposals = self.proposal_generator.get_all_proposals()
        self.assertEqual(len(all_proposals), 2)


if __name__ == '__main__':
    unittest.main()
