import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.proposal import Proposal
from models.github_project import GitHubProject


class TestProposal(unittest.TestCase):
    
    def test_proposal_initialization(self):
        """Test proposal creation with string conclusions."""
        proposal = Proposal(
            title="Test Proposal", 
            description="This is a test description.", 
            conclusions="Conclusion 1\nConclusion 2"
        )
        self.assertEqual(proposal.title, "Test Proposal")
        self.assertEqual(proposal.description, "This is a test description.")
        self.assertEqual(len(proposal.conclusions_list), 2)
        self.assertIn("Conclusion 1", proposal.conclusions_list)
        self.assertIn("Conclusion 2", proposal.conclusions_list)

    def test_proposal_validation_success(self):
        """Test successful proposal validation."""
        proposal = Proposal(
            title="Valid Title", 
            description="This is a valid description with sufficient length.", 
            conclusions="Valid conclusion 1\nValid conclusion 2"
        )
        self.assertTrue(proposal.is_valid())

    def test_proposal_validation_failure(self):
        """Test proposal validation failures."""
        # Empty title
        proposal = Proposal(
            title="", 
            description="This is a test description with sufficient length.", 
            conclusions="Conclusion 1"
        )
        self.assertFalse(proposal.is_valid())
        
        # Short title
        proposal = Proposal(
            title="A", 
            description="This is a test description with sufficient length.", 
            conclusions="Conclusion 1"
        )
        self.assertFalse(proposal.is_valid())

    def test_proposal_format(self):
        """Test proposal formatting."""
        proposal = Proposal(
            title="Test Title", 
            description="Test description", 
            conclusions="Conclusion 1\nConclusion 2"
        )
        formatted = proposal.format_proposal()
        self.assertIn("Test Title", formatted)
        self.assertIn("Test description", formatted)
        self.assertIn("- Conclusion 1", formatted)
        self.assertIn("- Conclusion 2", formatted)

    def test_proposal_to_dict(self):
        """Test proposal dictionary conversion."""
        proposal = Proposal(
            title="Test Title", 
            description="Test description", 
            conclusions="Conclusion 1\nConclusion 2"
        )
        data = proposal.to_dict()
        self.assertEqual(data['title'], "Test Title")
        self.assertEqual(data['description'], "Test description")
        self.assertEqual(len(data['conclusions']), 2)


class TestGitHubProject(unittest.TestCase):
    
    def test_github_project_initialization(self):
        """Test GitHub project initialization with minimal data."""
        project = GitHubProject(
            name="test-repo",
            full_name="user/test-repo",
            html_url="https://github.com/user/test-repo",
            description="A test project."
        )
        self.assertEqual(project.name, "test-repo")
        self.assertEqual(project.full_name, "user/test-repo")
        self.assertEqual(project.html_url, "https://github.com/user/test-repo")
        self.assertEqual(project.description, "A test project.")

    def test_github_project_from_api_response(self):
        """Test creating project from API response."""
        api_data = {
            'name': 'test-repo',
            'full_name': 'user/test-repo',
            'html_url': 'https://github.com/user/test-repo',
            'description': 'A test repository',
            'language': 'Python',
            'stargazers_count': 100,
            'forks_count': 20,
            'open_issues_count': 5
        }
        project = GitHubProject.from_api_response(api_data)
        self.assertEqual(project.name, 'test-repo')
        self.assertEqual(project.language, 'Python')
        self.assertEqual(project.stargazers_count, 100)

    def test_github_project_stats(self):
        """Test project statistics formatting."""
        project = GitHubProject(
            name="test-repo",
            language="Python",
            stargazers_count=150,
            forks_count=30,
            open_issues_count=8
        )
        stats = project.get_project_stats()
        self.assertIn("Python", stats)
        self.assertIn("150", stats)
        self.assertIn("30", stats)
        self.assertIn("8", stats)

    def test_github_project_to_dict(self):
        """Test project dictionary conversion."""
        project = GitHubProject(
            name="test-repo",
            full_name="user/test-repo",
            language="Python",
            stargazers_count=100
        )
        data = project.to_dict()
        self.assertEqual(data['name'], "test-repo")
        self.assertEqual(data['language'], "Python")
        self.assertEqual(data['stargazers_count'], 100)


if __name__ == '__main__':
    unittest.main()
