// GitHub Proposal Generator - Frontend JavaScript

class ProposalGenerator {
  constructor() {
    this.currentStep = 1;
    this.maxSteps = 2;
    this.selectedRepository = null;
    this.searchResults = [];
    this.init();
  }

  init() {
    this.bindEvents();
    this.setupCharacterCounters();
    this.setupFormValidation();
  }

  bindEvents() {
    // Step navigation
    document.getElementById('nextStep1').addEventListener('click', () => {
      this.searchRepositories();
    });

    document.getElementById('prevStep2').addEventListener('click', () => {
      this.goToStep(1);
    });

    // Form submission
    document.getElementById('proposalForm').addEventListener('submit', (e) => {
      e.preventDefault();
      this.generateProposal();
    });

    // Result actions
    document.getElementById('copyProposal').addEventListener('click', () => {
      this.copyToClipboard();
    });

    document.getElementById('saveProposal').addEventListener('click', () => {
      this.saveProposal();
    });

    document.getElementById('newProposal').addEventListener('click', () => {
      this.resetForm();
    });

    // Input validation for step 1
    const step1Inputs = ['title', 'description', 'conclusions'];
    step1Inputs.forEach(inputId => {
      const input = document.getElementById(inputId);
      input.addEventListener('input', () => {
        this.validateStep1();
      });
    });
  }

  setupCharacterCounters() {
    const titleInput = document.getElementById('title');
    const descriptionInput = document.getElementById('description');
    const titleCounter = document.getElementById('titleCounter');
    const descriptionCounter = document.getElementById('descriptionCounter');

    titleInput.addEventListener('input', () => {
      const count = titleInput.value.length;
      titleCounter.textContent = count;
      titleCounter.style.color = count > 90 ? 'var(--error-color)' : 'var(--text-muted)';
    });

    descriptionInput.addEventListener('input', () => {
      const count = descriptionInput.value.length;
      descriptionCounter.textContent = count;
      descriptionCounter.style.color = count > 950 ? 'var(--error-color)' : 'var(--text-muted)';
    });
  }

  setupFormValidation() {
    const inputs = ['title', 'description', 'conclusions'];
    inputs.forEach(inputId => {
      const input = document.getElementById(inputId);
      input.addEventListener('input', () => {
        this.validateInput(input);
      });
      input.addEventListener('blur', () => {
        this.validateInput(input);
      });
    });
  }

  validateInput(input) {
    const value = input.value.trim();
    const minLength = input.id === 'title' ? 5 : 10;

    input.classList.remove('error', 'success');

    if (value.length === 0) {
      return;
    } else if (value.length < minLength) {
      input.classList.add('error');
      input.style.borderColor = 'var(--error-color)';
    } else {
      input.classList.add('success');
      input.style.borderColor = 'var(--success-color)';
    }
  }

  validateStep1() {
    const title = document.getElementById('title').value.trim();
    const description = document.getElementById('description').value.trim();
    const conclusions = document.getElementById('conclusions').value.trim();

    const isValid = title.length >= 5 && description.length >= 10 && conclusions.length >= 5;
    document.getElementById('nextStep1').disabled = !isValid;

    return isValid;
  }

  async searchRepositories() {
    if (!this.validateStep1()) {
      this.showToast('Please fill in all required fields with valid content', 'error');
      return;
    }

    const formData = {
      title: document.getElementById('title').value.trim(),
      description: document.getElementById('description').value.trim(),
      conclusions: document.getElementById('conclusions').value.trim(),
      language: document.getElementById('language').value.trim()
    };

    this.showLoading('Searching for relevant repositories...');

    try {
      const response = await fetch('/api/search-repositories', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (response.ok && data.success) {
        this.searchResults = data.repositories;
        this.displaySearchResults(data);
        this.goToStep(2);
        this.showToast(`Found ${data.repositories.length} relevant repositories!`, 'success');
      } else {
        this.showToast(data.error || 'Failed to search repositories', 'error');
      }
    } catch (error) {
      console.error('Search error:', error);
      this.showToast('Network error. Please try again.', 'error');
    } finally {
      this.hideLoading();
    }
  }

  displaySearchResults(searchData) {
    const searchQuery = document.getElementById('searchQuery');
    const searchCount = document.getElementById('searchCount');
    const repositoryList = document.getElementById('repositoryList');

    // Update search info
    searchQuery.textContent = `Search terms: "${searchData.search_query}"`;
    searchCount.textContent = `Found ${searchData.repositories.length} repositories (${searchData.total_count.toLocaleString()} total matches)`;

    // Clear previous results
    repositoryList.innerHTML = '';

    if (searchData.repositories.length === 0) {
      repositoryList.innerHTML = `
                <div class="no-results">
                    <i class="fas fa-search"></i>
                    <h4>No repositories found</h4>
                    <p>Try adjusting your proposal content or language filter</p>
                </div>
            `;
      return;
    }

    // Create repository cards
    searchData.repositories.forEach((repo, index) => {
      const card = this.createRepositoryCard(repo, index);
      repositoryList.appendChild(card);
    });
  }

  createRepositoryCard(repo, index) {
    const card = document.createElement('div');
    card.className = 'repository-card';
    card.dataset.repoIndex = index;

    // Create topics HTML
    const topicsHtml = repo.topics && repo.topics.length > 0
      ? `<div class="repository-topics">
                ${repo.topics.slice(0, 3).map(topic => `<span class="topic-tag">${topic}</span>`).join('')}
               </div>`
      : '';

    card.innerHTML = `
            <div class="repository-header">
                <h6 class="repository-title">${repo.full_name}</h6>
                <a href="${repo.url}" target="_blank" class="btn btn-small">
                    <i class="fas fa-external-link-alt"></i>
                </a>
            </div>
            <p class="repository-description">${repo.description}</p>
            <div class="repository-meta">
                <span class="stat">
                    <i class="fas fa-code"></i>
                    ${repo.language || 'N/A'}
                </span>
                <span class="stat">
                    <i class="fas fa-star"></i>
                    ${this.formatNumber(repo.stars)}
                </span>
                <span class="stat">
                    <i class="fas fa-code-branch"></i>
                    ${this.formatNumber(repo.forks)}
                </span>
                <span class="stat">
                    <i class="fas fa-exclamation-circle"></i>
                    ${this.formatNumber(repo.issues)}
                </span>
            </div>
            ${topicsHtml}
        `;

    // Add click handler
    card.addEventListener('click', (e) => {
      // Don't trigger if clicking the external link
      if (e.target.closest('a')) return;

      this.selectRepository(repo, card);
    });

    return card;
  }

  selectRepository(repo, cardElement) {
    // Remove previous selection
    document.querySelectorAll('.repository-card').forEach(card => {
      card.classList.remove('selected');
    });

    // Add selection to clicked card
    cardElement.classList.add('selected');

    // Store selected repository
    this.selectedRepository = repo;

    // Display selected repository info
    this.displaySelectedRepository(repo);

    // Enable generate button
    document.getElementById('generateProposal').disabled = false;
  }

  displaySelectedRepository(repo) {
    document.getElementById('selectedRepoName').textContent = repo.full_name;
    document.getElementById('selectedRepoDescription').textContent = repo.description;
    document.getElementById('selectedRepoLanguage').textContent = repo.language || 'N/A';
    document.getElementById('selectedRepoStars').textContent = this.formatNumber(repo.stars);
    document.getElementById('selectedRepoForks').textContent = this.formatNumber(repo.forks);
    document.getElementById('selectedRepoIssues').textContent = this.formatNumber(repo.issues);
    document.getElementById('selectedRepoUrl').href = repo.url;

    const selectedRepoInfo = document.getElementById('selectedRepoInfo');
    selectedRepoInfo.classList.remove('hidden');
    setTimeout(() => {
      selectedRepoInfo.classList.add('visible');
    }, 100);
  }

  formatNumber(num) {
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'k';
    }
    return num.toString();
  }

  goToStep(step) {
    if (step < 1 || step > this.maxSteps) return;

    // Hide current step
    document.getElementById(`step${this.currentStep}`).classList.remove('active');

    // Show new step
    document.getElementById(`step${step}`).classList.add('active');

    this.currentStep = step;

    // Update progress indicator
    this.updateProgressIndicator(step);

    // Scroll to top of form
    document.querySelector('.form-section').scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    });
  }

  updateProgressIndicator(currentStep) {
    // Reset all progress steps
    for (let i = 1; i <= 3; i++) {
      const progressStep = document.getElementById(`progressStep${i}`);
      progressStep.classList.remove('active', 'completed');

      if (i < currentStep) {
        progressStep.classList.add('completed');
      } else if (i === currentStep) {
        progressStep.classList.add('active');
      }
    }

    // Update progress lines
    const progressLines = document.querySelectorAll('.progress-line');
    progressLines.forEach((line, index) => {
      if (index < currentStep - 1) {
        line.classList.add('completed');
      } else {
        line.classList.remove('completed');
      }
    });
  }

  async generateProposal() {
    if (!this.selectedRepository) {
      this.showToast('Please select a repository first', 'error');
      return;
    }

    const formData = {
      title: document.getElementById('title').value.trim(),
      description: document.getElementById('description').value.trim(),
      conclusions: document.getElementById('conclusions').value.trim(),
      repo_name: this.selectedRepository.full_name
    };

    this.showLoading('Generating your proposal...');

    try {
      const response = await fetch('/api/generate-proposal', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (response.ok && data.success) {
        this.displayProposal(data.proposal, data.metadata);
        this.updateProgressIndicator(3); // Move to step 3 (completed)
        this.showToast('Proposal generated successfully!', 'success');
      } else {
        this.showToast(data.error || 'Failed to generate proposal', 'error');
      }
    } catch (error) {
      console.error('Generation error:', error);
      this.showToast('Network error. Please try again.', 'error');
    } finally {
      this.hideLoading();
    }
  }

  displayProposal(proposalContent, metadata) {
    // Format proposal content for better display
    const proposalElement = document.getElementById('proposalContent');

    // Convert line breaks to proper HTML formatting
    const formattedContent = proposalContent
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br>');

    proposalElement.innerHTML = `<p>${formattedContent}</p>`;

    const resultsSection = document.getElementById('resultsSection');
    resultsSection.classList.remove('hidden');

    setTimeout(() => {
      resultsSection.classList.add('visible');
      resultsSection.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }, 100);

    // Store proposal data for saving
    this.currentProposal = {
      content: proposalContent,
      metadata: metadata
    };
  }

  async copyToClipboard() {
    if (!this.currentProposal) {
      this.showToast('No proposal to copy', 'error');
      return;
    }

    try {
      await navigator.clipboard.writeText(this.currentProposal.content);
      this.showToast('Proposal copied to clipboard!', 'success');
    } catch (error) {
      console.error('Copy error:', error);
      this.showToast('Failed to copy to clipboard', 'error');
    }
  }

  async saveProposal() {
    if (!this.currentProposal) {
      this.showToast('No proposal to save', 'error');
      return;
    }

    const filename = prompt('Enter filename (without extension):',
      `proposal_${new Date().toISOString().slice(0, 10)}`);

    if (!filename) return;

    this.showLoading('Saving proposal...');

    try {
      const response = await fetch('/api/save-proposal', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: this.currentProposal.content,
          filename: filename
        })
      });

      const data = await response.json();

      if (response.ok && data.success) {
        this.showToast(`Proposal saved as ${data.filename}`, 'success');
      } else {
        this.showToast(data.error || 'Failed to save proposal', 'error');
      }
    } catch (error) {
      console.error('Save error:', error);
      this.showToast('Network error. Please try again.', 'error');
    } finally {
      this.hideLoading();
    }
  }

  resetForm() {
    // Reset all form fields
    document.getElementById('proposalForm').reset();

    // Reset validation states
    this.selectedRepository = null;
    this.searchResults = [];
    this.currentStep = 1;
    this.currentProposal = null;

    // Reset UI states
    document.getElementById('step2').classList.remove('active');
    document.getElementById('step1').classList.add('active');
    document.getElementById('nextStep1').disabled = true;
    document.getElementById('generateProposal').disabled = true;
    document.getElementById('selectedRepoInfo').classList.add('hidden');
    document.getElementById('resultsSection').classList.add('hidden');
    document.getElementById('resultsSection').classList.remove('visible');

    // Clear search results
    document.getElementById('repositoryList').innerHTML = '';

    // Reset character counters
    document.getElementById('titleCounter').textContent = '0';
    document.getElementById('descriptionCounter').textContent = '0';

    // Reset progress indicator
    this.updateProgressIndicator(1);

    // Reset input styling
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
      input.classList.remove('error', 'success');
      input.style.borderColor = '';
    });

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });

    this.showToast('Form reset successfully', 'info');
  }

  showLoading(message = 'Loading...') {
    document.getElementById('loadingMessage').textContent = message;
    document.getElementById('loadingModal').classList.add('active');
  }

  hideLoading() {
    document.getElementById('loadingModal').classList.remove('active');
  }

  showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');

    setTimeout(() => {
      toast.classList.remove('show');
    }, 4000);
  }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new ProposalGenerator();
});

// Add some CSS classes dynamically for better UX
const style = document.createElement('style');
style.textContent = `
    .form-group input.error,
    .form-group textarea.error,
    .form-group select.error {
        border-color: var(--error-color) !important;
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1) !important;
    }
    
    .form-group input.success,
    .form-group textarea.success,
    .form-group select.success {
        border-color: var(--success-color) !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1) !important;
    }
    
    #selectedRepoInfo,
    #resultsSection {
        display: none;
    }
    
    #selectedRepoInfo.visible,
    #resultsSection.visible {
        display: block;
    }
`;
document.head.appendChild(style);
