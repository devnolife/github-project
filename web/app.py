import sys
import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import json
from datetime import datetime
import requests
import urllib.parse

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from models.proposal import Proposal
from models.github_project import GitHubProject
from services.github_api import GitHubAPI, GitHubAPIError
from services.proposal_generator import ProposalGenerator
from utils.validators import validate_and_sanitize_proposal, validate_github_repo_name
from config.settings import PROJECT_NAME

app = Flask(__name__)
CORS(app)

# Configure Flask
app.config['SECRET_KEY'] = 'github-proposal-generator-secret-key'
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def index():
    """Main page route."""
    return render_template('index.html', project_name=PROJECT_NAME)

@app.route('/api/validate-repo', methods=['POST'])
def validate_repo():
    """Validate GitHub repository and fetch basic info."""
    try:
        data = request.get_json()
        repo_name = data.get('repo_name', '').strip()
        
        if not repo_name:
            return jsonify({'error': 'Repository name is required'}), 400
        
        # Validate repository name format
        try:
            validate_github_repo_name(repo_name)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        # Fetch repository data
        github_api = GitHubAPI()
        project_data = github_api.fetch_project_data(repo_name)
        github_project = GitHubProject.from_api_response(project_data)
        
        return jsonify({
            'valid': True,
            'project_info': {
                'name': github_project.name,
                'full_name': github_project.full_name,
                'description': github_project.description,
                'language': github_project.language,
                'stars': github_project.stargazers_count,
                'forks': github_project.forks_count,
                'issues': github_project.open_issues_count,
                'url': github_project.html_url,
                'created_at': github_project.get_formatted_date(github_project.created_at)
            }
        })
        
    except GitHubAPIError as e:
        return jsonify({'error': f'GitHub API Error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/generate-proposal', methods=['POST'])
def generate_proposal():
    """Generate proposal based on user input and GitHub project."""
    try:
        data = request.get_json()
        
        # Extract data
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        conclusions = data.get('conclusions', '').strip()
        repo_name = data.get('repo_name', '').strip()
        
        # Validate inputs
        if not all([title, description, conclusions, repo_name]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Validate and sanitize proposal data
        try:
            clean_title, clean_description, clean_conclusions = validate_and_sanitize_proposal(
                title, description, conclusions
            )
        except ValueError as e:
            return jsonify({'error': f'Validation Error: {str(e)}'}), 400
        
        # Validate repository name
        try:
            validate_github_repo_name(repo_name)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        # Create proposal instance
        proposal = Proposal(title=clean_title, description=clean_description, conclusions=clean_conclusions)
        
        if not proposal.is_valid():
            return jsonify({'error': 'Invalid proposal data'}), 400
        
        # Fetch GitHub project data
        github_api = GitHubAPI()
        project_data = github_api.fetch_project_data(repo_name)
        github_project = GitHubProject.from_api_response(project_data)
        
        # Generate proposal
        proposal_generator = ProposalGenerator()
        generated_proposal = proposal_generator.generate(proposal, github_project)
        
        return jsonify({
            'success': True,
            'proposal': generated_proposal,
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'project_name': github_project.full_name,
                'project_url': github_project.html_url
            }
        })
        
    except GitHubAPIError as e:
        return jsonify({'error': f'GitHub API Error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/save-proposal', methods=['POST'])
def save_proposal():
    """Save proposal to file."""
    try:
        data = request.get_json()
        proposal_content = data.get('content', '')
        filename = data.get('filename', '')
        
        if not proposal_content:
            return jsonify({'error': 'Proposal content is required'}), 400
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"proposal_{timestamp}.md"
        
        # Ensure filename ends with .md
        if not filename.endswith('.md'):
            filename += '.md'
        
        # Save to proposals directory
        proposals_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'proposals')
        os.makedirs(proposals_dir, exist_ok=True)
        
        filepath = os.path.join(proposals_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(proposal_content)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': filepath
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to save proposal: {str(e)}'}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'project': PROJECT_NAME,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/search-repositories', methods=['POST'])
def search_repositories():
    """Search GitHub repositories based on proposal content."""
    try:
        data = request.get_json()
        
        # Extract search criteria from proposal
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        conclusions = data.get('conclusions', '').strip()
        language = data.get('language', '').strip()
        
        if not any([title, description, conclusions]):
            return jsonify({'error': 'At least one field is required for search'}), 400
        
        # Build search query
        search_terms = []
        if title:
            search_terms.extend(title.split()[:3])  # Take first 3 words from title
        if description:
            search_terms.extend(description.split()[:5])  # Take first 5 words from description
        if conclusions:
            # Extract key terms from conclusions
            conclusion_words = conclusions.replace('\n', ' ').replace(';', ' ').split()
            search_terms.extend(conclusion_words[:3])
        
        # Remove common words and duplicates
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'}
        search_terms = list(set([term.lower().strip('.,!?;:') for term in search_terms if len(term) > 2 and term.lower() not in stop_words]))
        
        if not search_terms:
            return jsonify({'error': 'No valid search terms found in proposal'}), 400
        
        # Construct GitHub search API query
        query = ' '.join(search_terms[:5])  # Limit to 5 terms
        if language:
            query += f' language:{language}'
        
        # Add additional filters for better results
        query += ' stars:>10 forks:>2'  # Only repos with some community engagement
        
        # Search GitHub repositories
        github_api = GitHubAPI()
        search_url = f"{github_api.base_url}/search/repositories"
        
        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': 10
        }
        
        headers = {}
        if github_api.api_key and github_api.api_key != "your_api_key_here":
            headers['Authorization'] = f'token {github_api.api_key}'
        headers['Accept'] = 'application/vnd.github.v3+json'
        
        response = requests.get(search_url, params=params, headers=headers, timeout=30)
        
        if response.status_code == 200:
            search_results = response.json()
            repositories = []
            
            for repo in search_results.get('items', [])[:10]:  # Limit to top 10 results
                repo_info = {
                    'name': repo['name'],
                    'full_name': repo['full_name'],
                    'description': repo['description'] or 'No description available',
                    'language': repo['language'],
                    'stars': repo['stargazers_count'],
                    'forks': repo['forks_count'],
                    'issues': repo['open_issues_count'],
                    'url': repo['html_url'],
                    'updated_at': repo['updated_at'],
                    'topics': repo.get('topics', [])
                }
                repositories.append(repo_info)
            
            return jsonify({
                'success': True,
                'repositories': repositories,
                'search_query': query,
                'total_count': min(search_results.get('total_count', 0), 1000)  # GitHub limits results
            })
        
        elif response.status_code == 403:
            return jsonify({'error': 'GitHub API rate limit exceeded. Please try again later.'}), 429
        else:
            return jsonify({'error': f'GitHub search failed with status {response.status_code}'}), 400
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Network error during search: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error during search: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Development server
    print(f"🚀 Starting {PROJECT_NAME} Web Server...")
    print("📝 Available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
