# automod_lover-bot

## Overview

automod_lover-bot is a Python Reddit bot that automatically monitors the r/UpvoteAutomod subreddit and responds with "Good bot" to AutoModerator comments. The bot continuously scans for new posts, switches to newer posts for optimal coverage, and maintains intelligent rate limiting to respect Reddit's API constraints while providing consistent automated responses.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Bot Architecture
The system implements a modular, single-threaded architecture built around three primary components:

- **Main Bot Controller**: Orchestrates the primary monitoring loop, handles Reddit API interactions, and manages post switching logic for optimal coverage
- **Configuration Manager**: Centralizes all bot settings including API credentials, timing parameters, and validation logic to ensure secure and configurable operation  
- **Rate Limit Parser**: Specialized component for parsing Reddit API error messages and extracting precise wait times to handle rate limiting gracefully

### Reddit API Integration
The bot leverages PRAW (Python Reddit API Wrapper) for all Reddit interactions, using OAuth2 script-type authentication to maintain a persistent connection throughout operation. This design choice provides reliable access to Reddit's API while handling authentication seamlessly.

### Error Handling and Rate Limiting
Implements intelligent rate limit detection by parsing Reddit API error messages using regex patterns. The system can extract wait times from various error message formats (minutes, seconds, hours) and automatically adjust delays to respect API constraints without manual intervention.

### State Management
Maintains in-memory state tracking including:
- Current target post ID for focused monitoring
- Set of previously replied-to comments to prevent duplicate responses
- Rate limit status and timing information for optimal API usage

### Operational Flow
The bot operates in a continuous monitoring loop:
1. Monitor r/UpvoteAutomod for newest posts
2. Switch to newer posts when they appear for maximum coverage
3. Scan current target post for AutoModerator comments
4. Reply "Good bot" to new AutoModerator comments
5. Implement intelligent delays between actions to respect rate limits
6. Handle errors gracefully and continue operation without interruption

### Logging and Monitoring
Employs Python's built-in logging module with dual output streams - file-based logging for persistence and console output for real-time monitoring. Comprehensive logging covers connection status, comment processing, rate limiting, and error handling.

## External Dependencies

### Reddit API (PRAW)
- **Purpose**: Primary interface for all Reddit interactions including authentication, post retrieval, comment scanning, and reply posting
- **Rate Limiting**: Handles Reddit's API rate limits through built-in mechanisms supplemented by custom parsing logic
- **Authentication**: Uses OAuth2 script-type credentials for secure API access

### Python Environment Management
- **python-dotenv**: Manages environment variables and configuration loading from .env files
- **Standard Library**: Utilizes built-in modules for logging, regular expressions, time management, and system operations