# AutomodLoverBot

A Python Reddit bot that monitors r/UpvoteAutomod and replies "Good bot" to AutoModerator comments.

## Features

- Monitors r/UpvoteAutomod for the newest posts (sorted by new)
- Finds AutoModerator comments in the current target post
- Replies "Good bot" to AutoModerator comments
- Implements 5-second delay between comment replies
- Switches monitoring to newer posts when they appear
- Intelligently handles Reddit API rate limits by parsing error messages
- Continuous operation with comprehensive logging

## Setup

### Prerequisites

- Python 3.7 or higher
- Reddit account for the bot (u/automod_lover-bot)
- Reddit API application credentials

### Installation

1. Clone or download this project
2. Install required packages:
   ```bash
   pip install praw python-dotenv
   ```

3. Create a Reddit application:
   - Go to https://www.reddit.com/prefs/apps/
   - Click "Create App" or "Create Another App"
   - Choose "script" as the app type
   - Note down your client ID and client secret

4. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your Reddit API credentials:
     ```bash
     REDDIT_CLIENT_ID=your_client_id_here
     REDDIT_CLIENT_SECRET=your_client_secret_here
     REDDIT_USERNAME=automod_lover-bot
     REDDIT_PASSWORD=your_bot_account_password
     ```

### Running the Bot

```bash
python main.py
