<img width="80" height="80" alt="automod_lover-bot" src="https://github.com/user-attachments/assets/86338a91-c0bc-4716-9dbe-c3ce48962d88" />

# automod_lover-bot

Made using [Replit](https://repl.it), automod_lover-bot is a Python Reddit bot designed to automatically monitor the r/UpvoteAutomod subreddit and respond with "Good bot" to AutoModerator comments, while respecting Reddit's API rate limits and handling errors properly.

## Architecture

### Reddit API Integration
The bot uses PRAW (Python Reddit API Wrapper) for all Reddit interactions, using OAuth2 script-type authentication to maintain a persistent connection throughout operation. This provides reliable access to Reddit's API while handling authentication automatically.

### Error Handling and Rate Limiting
Implements intelligent rate limit detection by parsing Reddit API error messages using regex patterns. The system can extract wait times from various error message formats (minutes, seconds, hours) and automatically adjust delays to respect Reddit's rate limits without manual intervention.

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
Employs Python's built-in logging module with dual output streams - file-based logging for persistence and console output for real-time monitoring. Comprehensive logging covers connection status, comment detection, rate limiting, and error handling.

## External Dependencies

### Reddit API (PRAW)
- **Purpose**: Primary interface for all Reddit interactions including authentication, post retrieval, comment scanning, and reply posting
- **Rate Limiting**: Handles Reddit's API rate limits through built-in mechanisms supplemented by custom parsing logic
- **Authentication**: Uses OAuth2 script-type credentials for secure API access

### Python Standard Library
- **os/dotenv**: Environment variable management for secure credential storage and configuration
- **logging**: Comprehensive logging system for monitoring bot activity and debugging
- **time**: Timing controls for rate limiting and operational delays
- **re**: Regular expression parsing for rate limit error message analysis

## Hosting location
The bot was hosted on PythonAnywhere, where it ran continuously.

## Update (2025/8/27)
The bot's third Reddit account got suspended, so I've decided to discontinue this project and quit making bots on Reddit, and as a result, I've archived this repository.