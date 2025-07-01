from typing import List, Dict, Any
from datetime import datetime
from models.proposal import Proposal
from models.github_project import GitHubProject


class ProposalGenerator:
    def __init__(self):
        self.proposals = []

    def generate(self, proposal: Proposal, github_project: GitHubProject) -> str:
        """
        Generate a comprehensive proposal based on user input and GitHub project data.
        
        Args:
            proposal: User's proposal with title, description, and conclusions
            github_project: GitHub project information
            
        Returns:
            Formatted proposal string
        """
        # Store the proposal
        proposal_data = {
            'user_proposal': proposal.to_dict(),
            'github_project': github_project.to_dict(),
            'generated_at': datetime.now().isoformat(),
            'formatted_proposal': None
        }
        
        # Generate the formatted proposal
        formatted_proposal = self._format_comprehensive_proposal(proposal, github_project)
        proposal_data['formatted_proposal'] = formatted_proposal
        
        self.proposals.append(proposal_data)
        
        return formatted_proposal

    def _format_comprehensive_proposal(self, proposal: Proposal, github_project: GitHubProject) -> str:
        """Format a comprehensive proposal combining user input and project data."""
        
        formatted_proposal = f"""
# {proposal.title}

## Project Information
**Repository:** {github_project.full_name}
**URL:** {github_project.html_url}
**Language:** {github_project.language or 'Not specified'}

## Project Statistics
- **Stars:** {github_project.stargazers_count:,}
- **Forks:** {github_project.forks_count:,}
- **Open Issues:** {github_project.open_issues_count:,}
- **Created:** {github_project.get_formatted_date(github_project.created_at)}
- **Last Updated:** {github_project.get_formatted_date(github_project.updated_at)}

## Project Description
{github_project.description}

## Proposal Description
{proposal.description}

## Objectives and Conclusions
"""
        
        for i, conclusion in enumerate(proposal.conclusions_list, 1):
            formatted_proposal += f"{i}. {conclusion}\n"
        
        formatted_proposal += f"""

## Project Context Analysis
This proposal is designed for the **{github_project.full_name}** repository, which is primarily written in **{github_project.language or 'multiple languages'}**. 

The project has demonstrated community engagement with **{github_project.stargazers_count:,} stars** and **{github_project.forks_count:,} forks**, indicating {"strong" if github_project.stargazers_count > 100 else "emerging"} community interest.

With **{github_project.open_issues_count} open issues**, there {"are active development opportunities" if github_project.open_issues_count > 0 else "appears to be stable maintenance"} that align with this proposal's objectives.

## Implementation Recommendations
Based on the project's characteristics and the stated objectives, the following implementation approach is recommended:

1. **Assessment Phase**: Review existing codebase and documentation
2. **Planning Phase**: Align proposal objectives with project roadmap
3. **Development Phase**: Implement changes following project conventions
4. **Testing Phase**: Ensure compatibility with existing functionality
5. **Documentation Phase**: Update relevant documentation and examples
6. **Community Engagement**: Collaborate with maintainers and contributors

## Expected Outcomes
The implementation of this proposal should result in:
- Enhanced project functionality aligned with stated objectives
- Improved user experience and community value
- Sustainable code changes that follow project best practices
- Clear documentation for future maintenance and development

---
*Proposal generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}*
"""
        
        return formatted_proposal.strip()

    def add_proposal(self, title: str, description: str, conclusions: List[str]) -> Dict[str, Any]:
        """Add a proposal to the internal storage (legacy method)."""
        proposal = {
            'title': title,
            'description': description,
            'conclusions': conclusions,
            'created_at': datetime.now().isoformat()
        }
        self.proposals.append(proposal)
        return proposal

    def format_proposal(self, proposal: Dict[str, Any]) -> str:
        """Format a proposal dictionary (legacy method)."""
        formatted_proposal = f"Title: {proposal['title']}\n"
        formatted_proposal += f"Description: {proposal['description']}\n"
        formatted_proposal += "Conclusions:\n"
        for conclusion in proposal['conclusions']:
            formatted_proposal += f"- {conclusion}\n"
        return formatted_proposal

    def get_all_proposals(self) -> List[Dict[str, Any]]:
        """Get all stored proposals."""
        return self.proposals

    def get_latest_proposal(self) -> Dict[str, Any]:
        """Get the most recently generated proposal."""
        return self.proposals[-1] if self.proposals else None

    def export_proposal_to_markdown(self, proposal_index: int = -1) -> str:
        """Export a proposal to markdown format."""
        if not self.proposals:
            return "No proposals available"
        
        proposal = self.proposals[proposal_index]
        return proposal.get('formatted_proposal', 'No formatted proposal available')
