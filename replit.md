# AutomodLoverBot

## Overview

AutomodLoverBot is a Python Reddit bot that monitors the r/UpvoteAutomod subreddit and automatically responds with "Good bot" to AutoModerator comments. The bot continuously monitors for new posts, switches to newer posts for maximum coverage, and implements intelligent rate limiting to respect Reddit's API constraints while maintaining persistent operation.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Bot Architecture
The bot follows a simple event-driven monitoring pattern with a continuous loop architecture. The main bot class (`AutomodLoverBot`) orchestrates all operations through a centralized control flow that monitors, processes, and responds to Reddit content in real-time.

### State Management
The bot maintains minimal in-memory state to track operational context:
- **Current Target Post**: Tracks which post is being actively monitored
- **Reply History**: Maintains a set of previously replied-to comments to prevent duplicates
- **Rate Limit Status**: Tracks timing information for optimal API usage

This stateless approach ensures the bot can recover gracefully from interruptions without requiring persistent data storage.

### Configuration Management
Uses a centralized configuration system (`BotConfig`) that loads settings from environment variables with fallback defaults. This approach separates sensitive credentials from code and allows easy deployment across different environments.

### Error Handling and Rate Limiting
Implements a sophisticated rate limit detection system using regex pattern matching to parse Reddit API error messages. The `RateLimitParser` component can extract wait times from various error message formats and convert them to standardized seconds for consistent handling.

### Logging and Monitoring
Employs dual-stream logging with both file persistence and console output for comprehensive monitoring. The logging system captures all bot activities including connection status, comment processing, rate limit events, and error conditions.

### Operational Flow
The bot operates in a continuous monitoring loop:
1. Monitors r/UpvoteAutomod for newest posts
2. Automatically switches to newer posts when they appear
3. Scans current target post for AutoModerator comments
4. Replies "Good bot" to new AutoModerator comments
5. Implements intelligent delays between actions
6. Handles errors gracefully and continues operation

## External Dependencies

### Reddit API (PRAW)
- **Purpose**: Primary interface for all Reddit interactions including authentication, post retrieval, comment scanning, and reply posting
- **Authentication**: Uses OAuth2 script-type credentials for secure API access
- **Rate Limiting**: Handles Reddit's built-in rate limits supplemented by custom parsing logic

### Python Standard Library
- **os/dotenv**: Environment variable management for secure credential storage
- **logging**: Comprehensive logging system for activity monitoring and debugging
- **time**: Timing controls for rate limiting and operational delays
- **re**: Regular expression parsing for rate limit error message analysis

### Hosting Platform
- **PythonAnywhere**: Cloud hosting platform where the bot runs continuously with persistent execution environment