# GitHub Proposal Generator

A modern web application that allows users to create professional proposals for GitHub projects. It features both a sleek web interface and a command-line interface, integrating with the GitHub API to fetch project details and generate comprehensive, structured proposals.

## ✨ Features

- 🌐 **Modern Web Interface** - Beautiful, responsive design with step-by-step form
- 📝 **Smart Proposal Generation** - AI-powered proposal creation with project analysis
- 🔍 **GitHub Integration** - Real-time repository validation and data fetching
- 📊 **Project Analytics** - Display repository statistics and information
- 💾 **Save & Export** - Save proposals as Markdown files
- 📱 **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- ⚡ **Real-time Validation** - Instant feedback on form inputs
- 🎯 **Professional Output** - Well-formatted proposals with implementation recommendations

## 🚀 Quick Start

### Web Interface (Recommended)

1. **Windows Users:**
   ```bash
   # Double-click or run in terminal
   run_web.bat
   ```

2. **Linux/Mac Users:**
   ```bash
   chmod +x run_web.sh
   ./run_web.sh
   ```

3. **Manual Launch:**
   ```bash
   python web_launcher.py
   ```

The web interface will automatically open in your browser at `http://localhost:5000`

### Command Line Interface

```bash
# For direct CLI usage
python cli.py
```

## 📁 Project Structure

```
github-proposal-generator
├── src/                       # Core application modules
│   ├── main.py               # CLI entry point
│   ├── models/               # Data models
│   │   ├── proposal.py       # Proposal model
│   │   └── github_project.py # GitHub project model
│   ├── services/             # Business logic
│   │   ├── github_api.py     # GitHub API integration
│   │   └── proposal_generator.py # Proposal generation
│   ├── utils/                # Utility functions
│   │   └── validators.py     # Input validation
│   └── config/               # Configuration
│       └── settings.py       # App settings
├── web/                      # Web interface
│   ├── app.py               # Flask web application
│   ├── templates/           # HTML templates
│   │   ├── index.html       # Main interface
│   │   ├── 404.html         # Error pages
│   │   └── 500.html
│   └── static/              # Static assets
│       ├── css/
│       │   └── style.css    # Modern CSS styling
│       └── js/
│           └── main.js      # Frontend JavaScript
├── tests/                   # Test suite
├── proposals/              # Generated proposals storage
├── requirements.txt        # Python dependencies
├── web_launcher.py        # Web interface launcher
├── run_web.bat           # Windows launcher
├── run_web.sh            # Linux/Mac launcher
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/github-proposal-generator.git
   ```
2. Navigate to the project directory:
   ```
   cd github-proposal-generator
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Set up your environment variables by copying `.env.example` to `.env` and filling in the necessary values.
2. Run the application:
   ```
   python src/main.py
   ```
3. Follow the prompts to input your conclusions or desires for the proposal.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
