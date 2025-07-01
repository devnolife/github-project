import sys
import os
from typing import Optional

# Add the src directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.proposal import Proposal
from models.github_project import GitHubProject
from services.github_api import GitHubAPI, GitHubAPIError
from services.proposal_generator import ProposalGenerator
from utils.validators import validate_and_sanitize_proposal, validate_github_repo_name
from config.settings import PROJECT_NAME


def print_header():
    """Print application header."""
    print("=" * 60)
    print(f"  {PROJECT_NAME}")
    print("=" * 60)
    print("Create structured proposals for GitHub projects")
    print()


def get_user_input() -> tuple:
    """Get and validate user input for the proposal."""
    print("📝 Enter your proposal details:")
    print()
    
    while True:
        try:
            title = input("Proposal Title: ").strip()
            if not title:
                print("❌ Title cannot be empty. Please try again.")
                continue
                
            description = input("\nProposal Description: ").strip()
            if not description:
                print("❌ Description cannot be empty. Please try again.")
                continue
                
            print("\nConclusions/Objectives (separate multiple items with new lines or semicolons):")
            conclusions = input("").strip()
            if not conclusions:
                print("❌ Conclusions cannot be empty. Please try again.")
                continue
            
            # Validate and sanitize inputs
            clean_title, clean_description, clean_conclusions = validate_and_sanitize_proposal(
                title, description, conclusions
            )
            
            return clean_title, clean_description, clean_conclusions
            
        except ValueError as e:
            print(f"❌ Validation Error: {e}")
            print("Please try again with valid input.\n")


def get_github_project() -> Optional[GitHubProject]:
    """Get GitHub project information."""
    print("\n🔍 Enter GitHub project details:")
    
    while True:
        project_name = input("\nGitHub Repository (format: owner/repo, e.g., 'facebook/react'): ").strip()
        
        if not project_name:
            print("❌ Repository name cannot be empty.")
            continue
            
        try:
            validate_github_repo_name(project_name)
            break
        except ValueError as e:
            print(f"❌ {e}")
            continue
    
    print(f"\n🌐 Fetching project data for '{project_name}'...")
    
    try:
        github_api = GitHubAPI()
        project_data = github_api.fetch_project_data(project_name)
        github_project = GitHubProject.from_api_response(project_data)
        
        print("✅ Project data fetched successfully!")
        print(f"\nProject: {github_project.full_name}")
        print(f"Description: {github_project.description}")
        print(f"Language: {github_project.language}")
        print(f"Stars: {github_project.stargazers_count:,}")
        
        return github_project
        
    except GitHubAPIError as e:
        print(f"❌ GitHub API Error: {e}")
        retry = input("\nWould you like to try with a different repository? (y/n): ").lower()
        if retry == 'y':
            return get_github_project()
        else:
            return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


def save_proposal_to_file(proposal_content: str, filename: str = None) -> Optional[str]:
    """Save proposal to a markdown file."""
    if not filename:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"proposal_{timestamp}.md"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(proposal_content)
        return filename
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return None


def main():
    """Main application function."""
    try:
        print_header()
        
        # Get user input for the proposal
        title, description, conclusions = get_user_input()
        
        # Create a Proposal instance
        proposal = Proposal(title=title, description=description, conclusions=conclusions)
        
        # Validate the proposal
        if not proposal.is_valid():
            print("❌ The proposal is not valid. Please check your input.")
            sys.exit(1)
        
        print("✅ Proposal created successfully!")
        
        # Get GitHub project details
        github_project = get_github_project()
        
        if not github_project:
            print("❌ Cannot proceed without valid GitHub project data.")
            sys.exit(1)
        
        # Generate the proposal
        print("\n📄 Generating comprehensive proposal...")
        proposal_generator = ProposalGenerator()
        generated_proposal = proposal_generator.generate(proposal, github_project)
        
        # Display the generated proposal
        print("\n" + "="*60)
        print("📋 GENERATED PROPOSAL")
        print("="*60)
        print(generated_proposal)
        print("="*60)
        
        # Ask if user wants to save to file
        save_to_file = input("\n💾 Would you like to save this proposal to a file? (y/n): ").lower()
        if save_to_file == 'y':
            filename = save_proposal_to_file(generated_proposal)
            if filename:
                print(f"✅ Proposal saved to '{filename}'")
            else:
                print("❌ Failed to save proposal to file")
        
        print("\n🎉 Thank you for using GitHub Proposal Generator!")
        
    except KeyboardInterrupt:
        print("\n\n👋 Application cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error occurred: {e}")
        print("Please try again or report this issue.")
        sys.exit(1)


if __name__ == "__main__":
    main()
