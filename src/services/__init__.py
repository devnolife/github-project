"""
Services package for GitHub Proposal Generator.

This package contains service classes for GitHub API interaction and proposal generation.
"""

from .github_api import GitHubAPI, GitHubAPIError
from .proposal_generator import ProposalGenerator

__all__ = ['GitHubAPI', 'GitHubAPIError', 'ProposalGenerator']
