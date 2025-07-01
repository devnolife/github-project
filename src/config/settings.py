import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_KEY = os.getenv('API_KEY', 'your_api_key_here')
GITHUB_API_URL = os.getenv('GITHUB_URL', 'https://api.github.com')

# Application Configuration
PROJECT_NAME = os.getenv('PROJECT_NAME', 'GitHub Proposal Generator')
USER_NAME = os.getenv('USER_NAME', 'your_github_username_here')

# Default Values
DEFAULT_PROPOSAL_TITLE = "Proposal for GitHub Project Enhancement"
DEFAULT_PROPOSAL_DESCRIPTION = "This proposal outlines the objectives and desired outcomes for improving the project."

# Validation Configuration
MAX_TITLE_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 1000
MIN_TITLE_LENGTH = 5
MIN_DESCRIPTION_LENGTH = 10

# Error Messages
VALIDATION_ERROR_MESSAGE = "Input validation failed. Please check your input and try again."
API_ERROR_MESSAGE = "Failed to fetch project data from GitHub API."
NETWORK_ERROR_MESSAGE = "Network connection error. Please check your internet connection."

# Output Configuration
OUTPUT_FORMAT = 'markdown'
INCLUDE_TIMESTAMPS = True
INCLUDE_PROJECT_STATS = True
