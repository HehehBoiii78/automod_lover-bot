# AutomodLoverBot

## Overview

AutomodLoverBot is a Python Reddit bot that automatically monitors the r/UpvoteAutomod subreddit and responds with "Good bot" to AutoModerator comments. The bot continuously scans for new posts, identifies AutoModerator comments within those posts, and replies appropriately while respecting Reddit's API rate limits. It features intelligent rate limit handling, comprehensive logging, and robust error recovery mechanisms to ensure continuous operation.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Bot Architecture
The system follows a modular, single-threaded architecture with three main components:

- **Main Bot Controller** (`main.py`): Orchestrates the bot's primary monitoring loop, handles Reddit API interactions, and manages post switching logic
- **Configuration Manager** (`config.py`): Centralizes all bot settings including API credentials, timing parameters, and validation logic
- **Rate Limit Parser** (`rate_limit_parser.py`): Specialized component for parsing Reddit API error messages and extracting precise wait times

### Reddit API Integration
Uses the PRAW (Python Reddit API Wrapper) library for all Reddit interactions. The bot authenticates using OAuth2 script-type credentials and maintains a persistent connection throughout its operation.

### Error Handling and Rate Limiting
Implements intelligent rate limit detection by parsing Reddit API error messages using regex patterns. The system can extract wait times from various error message formats (minutes, seconds, hours) and automatically pause execution for the appropriate duration.

### Logging and Monitoring
Employs Python's built-in logging module with dual output streams - both file-based logging for persistence and console output for real-time monitoring. Comprehensive logging covers connection status, comment detection, reply attempts, and error conditions.

### State Management
Maintains in-memory state tracking including:
- Current target post ID for monitoring
- Set of previously replied-to comments to prevent duplicates
- Rate limit status and timing information

### Operational Flow
The bot operates in a continuous loop:
1. Monitor r/UpvoteAutomod for newest posts
2. Switch to newer posts when they appear
3. Scan current target post for AutoModerator comments
4. Reply "Good bot" to new AutoModerator comments
5. Implement delays between actions to respect rate limits
6. Handle errors gracefully and continue operation

## External Dependencies

### Reddit API (PRAW)
- **Purpose**: Primary interface for all Reddit interactions
- **Functionality**: Authentication, post retrieval, comment scanning, and reply posting
- **Rate Limiting**: Handles Reddit's API rate limits through built-in mechanisms

### Python Standard Library
- **os/dotenv**: Environment variable management for secure credential storage
- **time**: Implements delays and timing controls between operations
- **logging**: Comprehensive logging and monitoring capabilities
- **datetime**: Timestamp generation for logging and operational tracking
- **re**: Regular expression parsing for rate limit error message analysis

### Environment Variables
- **REDDIT_CLIENT_ID**: Reddit application client identifier
- **REDDIT_CLIENT_SECRET**: Reddit application secret key
- **REDDIT_USERNAME**: Bot account username (automod_lover-bot)
- **REDDIT_PASSWORD**: Bot account password

### File System Dependencies
- **Configuration Files**: `.env` for environment variables, `.env.example` as template
- **Log Files**: `automod_lover_bot.log` for persistent operation logging
- **Runtime Files**: No database dependencies - all state maintained in memory