import re
from typing import List
from config.settings import MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH, MIN_TITLE_LENGTH, MIN_DESCRIPTION_LENGTH


def is_valid_title(title: str) -> bool:
    """Validate proposal title."""
    if not isinstance(title, str):
        return False
    title = title.strip()
    return MIN_TITLE_LENGTH <= len(title) <= MAX_TITLE_LENGTH


def is_valid_description(description: str) -> bool:
    """Validate proposal description."""
    if not isinstance(description, str):
        return False
    description = description.strip()
    return MIN_DESCRIPTION_LENGTH <= len(description) <= MAX_DESCRIPTION_LENGTH


def is_valid_conclusions(conclusions: List[str]) -> bool:
    """Validate conclusions list."""
    if not isinstance(conclusions, list):
        return False
    if len(conclusions) == 0:
        return False
    return all(isinstance(conclusion, str) and len(conclusion.strip()) > 0 for conclusion in conclusions)


def is_valid_github_repo_name(repo_name: str) -> bool:
    """Validate GitHub repository name format (owner/repo)."""
    if not isinstance(repo_name, str):
        return False
    
    # GitHub repo pattern: owner/repo
    pattern = r'^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$'
    return bool(re.match(pattern, repo_name.strip()))


def validate_proposal_data(title: str, description: str, conclusions: List[str]) -> bool:
    """
    Validate all proposal data.
    
    Args:
        title: Proposal title
        description: Proposal description  
        conclusions: List of conclusions
        
    Returns:
        True if all data is valid
        
    Raises:
        ValueError: If any validation fails
    """
    if not is_valid_title(title):
        raise ValueError(f"Title must be a string between {MIN_TITLE_LENGTH} and {MAX_TITLE_LENGTH} characters.")
    
    if not is_valid_description(description):
        raise ValueError(f"Description must be a string between {MIN_DESCRIPTION_LENGTH} and {MAX_DESCRIPTION_LENGTH} characters.")
    
    if not is_valid_conclusions(conclusions):
        raise ValueError("Conclusions must be a non-empty list of non-empty strings.")
    
    return True


def validate_github_repo_name(repo_name: str) -> bool:
    """
    Validate GitHub repository name.
    
    Args:
        repo_name: Repository name in format 'owner/repo'
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If validation fails
    """
    if not is_valid_github_repo_name(repo_name):
        raise ValueError("Repository name must be in format 'owner/repo' (e.g., 'facebook/react')")
    
    return True


def sanitize_input(text: str) -> str:
    """Sanitize user input by stripping whitespace and removing excessive spaces."""
    if not isinstance(text, str):
        return ""
    
    # Strip leading/trailing whitespace and normalize internal whitespace
    return re.sub(r'\s+', ' ', text.strip())


def validate_and_sanitize_proposal(title: str, description: str, conclusions: str) -> tuple:
    """
    Validate and sanitize all proposal inputs.
    
    Args:
        title: Raw title input
        description: Raw description input
        conclusions: Raw conclusions input
        
    Returns:
        Tuple of (sanitized_title, sanitized_description, sanitized_conclusions)
        
    Raises:
        ValueError: If validation fails
    """
    # Sanitize inputs
    clean_title = sanitize_input(title)
    clean_description = sanitize_input(description)
    clean_conclusions = sanitize_input(conclusions)
    
    # Parse conclusions into list
    conclusions_list = [item.strip() for item in clean_conclusions.replace(';', '\n').split('\n')]
    conclusions_list = [item for item in conclusions_list if item]
    
    # Validate
    validate_proposal_data(clean_title, clean_description, conclusions_list)
    
    return clean_title, clean_description, clean_conclusions
