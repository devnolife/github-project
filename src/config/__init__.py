"""
Configuration package for GitHub Proposal Generator.

This package contains application settings and configuration.
"""

from .settings import *

__all__ = [
    'API_KEY',
    'GITHUB_API_URL',
    'PROJECT_NAME',
    'USER_NAME',
    'DEFAULT_PROPOSAL_TITLE',
    'DEFAULT_PROPOSAL_DESCRIPTION',
    'MAX_TITLE_LENGTH',
    'MAX_DESCRIPTION_LENGTH',
    'MIN_TITLE_LENGTH',
    'MIN_DESCRIPTION_LENGTH'
]
