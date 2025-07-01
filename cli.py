#!/usr/bin/env python3
"""
Command-line interface for GitHub Proposal Generator.

This script provides a command-line interface for generating proposals
with additional options and features.
"""

import argparse
import sys
import os
import json
from datetime import datetime

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from models.proposal import Proposal
from models.github_project import GitHubProject
from services.github_api import GitHubAPI, GitHubAPIError
from services.proposal_generator import ProposalGenerator
from utils.validators import validate_and_sanitize_proposal, validate_github_repo_name


def create_parser():
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description='Generate structured proposals for GitHub projects',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py facebook/react "Improve Documentation" "Enhance the documentation for better developer experience" "Add more examples; Improve API docs"
  
  python cli.py --interactive
  
  python cli.py microsoft/vscode "Add Feature" "Add new feature to improve user experience" "Implement feature X; Add tests; Update docs" --output proposal.md
        """
    )
    
    parser.add_argument(
        'repository',
        nargs='?',
        help='GitHub repository in format owner/repo (e.g., facebook/react)'
    )
    
    parser.add_argument(
        'title',
        nargs='?',
        help='Proposal title'
    )
    
    parser.add_argument(
        'description',
        nargs='?',
        help='Proposal description'
    )
    
    parser.add_argument(
        'conclusions',
        nargs='?',
        help='Conclusions/objectives separated by semicolons'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: auto-generated)'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )
    
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Do not save to file, only print to stdout'
    )
    
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate inputs without generating proposal'
    )
    
    return parser


def interactive_mode():
    """Run the application in interactive mode."""
    from main import main
    main()


def validate_inputs(repository, title, description, conclusions):
    """Validate all inputs and return sanitized versions."""
    try:
        validate_github_repo_name(repository)
        clean_title, clean_description, clean_conclusions = validate_and_sanitize_proposal(
            title, description, conclusions
        )
        return clean_title, clean_description, clean_conclusions
    except ValueError as e:
        print(f"❌ Validation Error: {e}")
        sys.exit(1)


def fetch_github_project(repository):
    """Fetch GitHub project data."""
    try:
        github_api = GitHubAPI()
        project_data = github_api.fetch_project_data(repository)
        return GitHubProject.from_api_response(project_data)
    except GitHubAPIError as e:
        print(f"❌ GitHub API Error: {e}")
        sys.exit(1)


def generate_proposal_content(title, description, conclusions, github_project):
    """Generate the proposal content."""
    proposal = Proposal(title=title, description=description, conclusions=conclusions)
    
    if not proposal.is_valid():
        print("❌ The proposal is not valid. Please check your input.")
        sys.exit(1)
    
    proposal_generator = ProposalGenerator()
    return proposal_generator.generate(proposal, github_project)


def save_to_file(content, output_path, is_json=False):
    """Save content to file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            if is_json:
                json.dump({"proposal": content, "generated_at": datetime.now().isoformat()}, f, indent=2)
            else:
                f.write(content)
        return output_path
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return None


def main():
    """Main CLI function."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive or (not args.repository and not args.title):
        interactive_mode()
        return
    
    # Validate required arguments
    if not all([args.repository, args.title, args.description, args.conclusions]):
        print("❌ Error: All arguments (repository, title, description, conclusions) are required in non-interactive mode.")
        parser.print_help()
        sys.exit(1)
    
    # Validate inputs
    print("🔍 Validating inputs...")
    title, description, conclusions = validate_inputs(
        args.repository, args.title, args.description, args.conclusions
    )
    
    if args.validate_only:
        print("✅ All inputs are valid!")
        return
    
    # Fetch GitHub project
    print(f"🌐 Fetching project data for '{args.repository}'...")
    github_project = fetch_github_project(args.repository)
    print(f"✅ Project data fetched: {github_project.full_name}")
    
    # Generate proposal
    print("📄 Generating proposal...")
    proposal_content = generate_proposal_content(title, description, conclusions, github_project)
    
    # Output
    if args.no_save:
        if args.json:
            output = {"proposal": proposal_content, "generated_at": datetime.now().isoformat()}
            print(json.dumps(output, indent=2))
        else:
            print(proposal_content)
    else:
        # Determine output file
        if args.output:
            output_file = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            extension = "json" if args.json else "md"
            output_file = f"proposal_{args.repository.replace('/', '_')}_{timestamp}.{extension}"
        
        # Save to file
        saved_file = save_to_file(proposal_content, output_file, args.json)
        if saved_file:
            print(f"✅ Proposal saved to '{saved_file}'")
        
        # Also print if not saving
        if not args.no_save:
            print("\n" + "="*60)
            print("📋 GENERATED PROPOSAL")
            print("="*60)
            print(proposal_content)


if __name__ == "__main__":
    main()
