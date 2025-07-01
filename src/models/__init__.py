"""
Models package for GitHub Proposal Generator.

This package contains data models for proposals and GitHub projects.
"""

from .proposal import Proposal
from .github_project import GitHubProject

__all__ = ['Proposal', 'GitHubProject']
