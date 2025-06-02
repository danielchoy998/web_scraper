# Reddit Scraper & AI Agent

## Description
A Python-based project that combines Reddit scraping capabilities with a LangGraph-powered AI agent. The system can autonomously scrape Reddit content and interact with users through a conversational interface with access to various tools.

## Components

### 1. Reddit Scraper (`reddit_scraper.py`)
- Uses PRAW to fetch Reddit submissions by ID or subreddit
- Downloads images via requests and OpenCV
- Saves comments to CSV with proper formatting
- Configurable rate limiting and data organization

### 2. AI Agent (`agent.py`)
- LangGraph-based conversational agent powered by OpenAI GPT-4
- Tool-calling capabilities with conditional execution flow
- Memory persistence across conversations
- Seamless integration with custom tools

### 3. Tool Suite (`tools.py`)
The agent has access to the following tools:

#### Core Tools:
- **`scrape_reddit(subreddit_name)`**: Scrapes a subreddit's top 5 posts including comments and images
- **`web_search(query)`**: Performs web search using TavilySearch API and returns top 2 results
- **`multiply(a, b)`**: Simple mathematical operation for testing
- **`human_assistance(query)`**: Requests human intervention when needed

## Features
- **Autonomous Reddit Data Collection**: Fetch and organize Reddit content automatically
- **Intelligent Conversation**: Natural language interaction with tool-calling capabilities
- **Multi-modal Data Handling**: Process text, images, and structured data
- **Extensible Architecture**: Easy to add new tools and capabilities
- **Memory Persistence**: Maintains conversation context across sessions
- **Human-in-the-loop**: Request human assistance when needed

## Prerequisites
- Python 3.8+
- Reddit App credentials (`CLIENT_ID`, `CLIENT_SECRET`, `USER_AGENT`)
- OpenAI API key for the agent
- Tavily API key for web search functionality

## Installation
```bash
git clone <repo_url>
cd scrapers
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration
Create a `.env` file in the project root:
```env
# Reddit API
CLIENT_ID=your_reddit_client_id
CLIENT_SECRET=your_reddit_client_secret
USER_AGENT=your_app/0.1 by u/your_username

# OpenAI API
OPENAI_API_KEY=your_openai_api_key

# Tavily Search API
TAVILY_API_KEY=your_tavily_api_key
```

## Usage

### Running the AI Agent
```bash
python agent.py
```
The agent will start a conversational interface where you can:
- Ask it to scrape specific subreddits
- Request web searches
- Get help with various tasks
- Request human assistance when needed

### Direct Reddit Scraping
```bash
python reddit_scraper.py
```

### Testing
```bash
python test.py  # Test the agent with human assistance functionality
python tools.py  # Test individual tools
```

## Output Structure
```
data/
├── reddit/
│   ├── images/          # Downloaded Reddit images (.jpg)
│   └── comments/        # Comment data (photo_review.csv)
```

## License
MIT License