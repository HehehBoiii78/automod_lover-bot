<img width="70" height="70" alt="automod_lover-bot" src="https://github.com/user-attachments/assets/7b7e6391-1471-4c7a-9c77-272d79d156c4" />

# automod_lover-bot

A Python Reddit bot that monitors r/UpvoteAutomod and replies "Good bot" to AutoModerator comments and works intelligently.

## Features

- Monitors the first post in r/UpvoteAutomod that appears when sorted by new
- Finds AutoModerator comments in the current target post
- Replies "Good bot" to any AutoModerator comments in the target post's thread
- Implements 5-second delay between comment replies
- Switches monitoring to newer posts when they appear
- Intelligently handles Reddit API rate limits by parsing error messages
- Continuous and efficient operation with comprehensive logging