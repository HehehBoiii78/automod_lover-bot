"""
Configuration module for AutomodLoverBot
Handles environment variables and bot settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class BotConfig:
    """Configuration class for bot settings."""
    
    def __init__(self):
        # Reddit API Credentials
        self.CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
        self.CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', '')
        self.USERNAME = os.getenv('REDDIT_USERNAME', 'automod_lover-bot')
        self.PASSWORD = os.getenv('REDDIT_PASSWORD', '')
        
        # Bot Configuration
        self.USER_AGENT = f"python:automod_lover_bot:v1.0 (by /u/{self.USERNAME})"
        self.TARGET_SUBREDDIT = 'UpvoteAutomod'
        self.TARGET_USER = 'AutoModerator'
        self.REPLY_MESSAGE = 'Good bot'
        
        # Timing Configuration
        self.COMMENT_DELAY = 5  # 5 seconds between comments
        self.MONITORING_INTERVAL = 10  # Check for new comments every 10 seconds
        self.ERROR_RETRY_DELAY = 30  # Wait 30 seconds after errors before retrying
        
        # Validate required credentials
        self._validate_credentials()
        
    def _validate_credentials(self):
        """Validate that required credentials are provided."""
        required_vars = [
            ('REDDIT_CLIENT_ID', self.CLIENT_ID),
            ('REDDIT_CLIENT_SECRET', self.CLIENT_SECRET),
            ('REDDIT_PASSWORD', self.PASSWORD)
        ]
        
        missing_vars = []
        for var_name, var_value in required_vars:
            if not var_value:
                missing_vars.append(var_name)
                
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}. "
                f"Please check your .env file or environment variables."
            )
