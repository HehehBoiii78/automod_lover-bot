#!/usr/bin/env python3
"""
Reddit Bot: automod_lover-bot
Monitors r/UpvoteAutomod for newest posts and replies "Good bot" to AutoModerator comments.
"""

import praw
import prawcore
import time
import logging
import os
import sys
from datetime import datetime
from config import BotConfig
from rate_limit_parser import RateLimitParser

class AutomodLoverBot:
    def __init__(self):
        """Initialize the bot with Reddit API connection and configuration."""
        self.config = BotConfig()
        self.rate_parser = RateLimitParser()
        self.logger = self._setup_logging()
        self.reddit = self._initialize_reddit()
        self.current_post_id = None
        self.replied_comments = set()
        
    def _setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('automod_lover_bot.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        return logging.getLogger('AutomodLoverBot')
        
    def _initialize_reddit(self):
        """Initialize Reddit API connection using PRAW."""
        try:
            reddit = praw.Reddit(
                client_id=self.config.CLIENT_ID,
                client_secret=self.config.CLIENT_SECRET,
                username=self.config.USERNAME,
                password=self.config.PASSWORD,
                user_agent=self.config.USER_AGENT
            )
            
            # Test the connection
            self.logger.info(f"Connected to Reddit as: {reddit.user.me()}")
            return reddit
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Reddit connection: {str(e)}")
            raise
            
    def get_newest_post(self):
        """Get the newest post from r/UpvoteAutomod."""
        try:
            subreddit = self.reddit.subreddit(self.config.TARGET_SUBREDDIT)
            newest_posts = list(subreddit.new(limit=1))
            
            if newest_posts:
                post = newest_posts[0]
                self.logger.info(f"Found newest post: {post.title} (ID: {post.id})")
                return post
            else:
                self.logger.warning("No posts found in subreddit")
                return None
                
        except Exception as e:
            self.logger.error(f"Error fetching newest post: {str(e)}")
            return None
            
    def find_automod_comments(self, post):
        """Find all comments by AutoModerator in the given post."""
        automod_comments = []
        try:
            # Refresh the post to get the latest comments
            post._fetch()
            post.comments.replace_more(limit=None)
            
            for comment in post.comments.list():
                if (comment.author and 
                    comment.author.name.lower() == self.config.TARGET_USER.lower() and
                    comment.id not in self.replied_comments):
                    automod_comments.append(comment)
                    
            self.logger.info(f"Found {len(automod_comments)} new AutoModerator comments to reply to")
            return automod_comments
            
        except Exception as e:
            self.logger.error(f"Error finding AutoModerator comments: {str(e)}")
            return []
            
    def reply_to_comment(self, comment):
        """Reply to a specific comment with rate limit handling."""
        try:
            self.logger.info(f"Attempting to reply to comment {comment.id}")
            
            # Reply to the comment
            reply = comment.reply(self.config.REPLY_MESSAGE)
            self.replied_comments.add(comment.id)
            
            self.logger.info(f"Successfully replied to comment {comment.id} with reply ID {reply.id}")
            return True
            
        except Exception as e:
            # Handle Reddit API exceptions, including rate limits
            error_message = str(e)
            self.logger.warning(f"Reddit API Exception: {error_message}")
            
            # Check if it's a rate limit error
            wait_time = self.rate_parser.parse_rate_limit_error(error_message)
            if wait_time > 0:
                self.logger.info(f"Rate limited. Waiting for {wait_time} seconds...")
                time.sleep(wait_time + self.config.COMMENT_DELAY)  # Add extra delay after rate limit
                
                # Retry the comment
                try:
                    reply = comment.reply(self.config.REPLY_MESSAGE)
                    self.replied_comments.add(comment.id)
                    self.logger.info(f"Successfully replied to comment {comment.id} after rate limit wait")
                    return True
                except Exception as retry_e:
                    self.logger.error(f"Failed to reply after rate limit wait: {str(retry_e)}")
                    return False
            else:
                self.logger.error(f"Failed to reply to comment {comment.id}: {error_message}")
                return False
            
    def monitor_post(self, post):
        """Monitor a specific post for new AutoModerator comments."""
        self.logger.info(f"Starting to monitor post: {post.title} (ID: {post.id})")
        
        while True:
            try:
                # Check if there's a newer post
                newest_post = self.get_newest_post()
                if newest_post and newest_post.id != post.id:
                    self.logger.info(f"Found newer post {newest_post.id}, switching monitoring target")
                    return newest_post
                    
                # Find AutoModerator comments in current post
                automod_comments = self.find_automod_comments(post)
                
                # Reply to each comment with delay
                for comment in automod_comments:
                    if self.reply_to_comment(comment):
                        self.logger.info(f"Waiting {self.config.COMMENT_DELAY} seconds before next comment...")
                        time.sleep(self.config.COMMENT_DELAY)
                        
                # Wait before checking for new comments again
                time.sleep(self.config.MONITORING_INTERVAL)
                
            except KeyboardInterrupt:
                self.logger.info("Bot stopped by user")
                raise
            except Exception as e:
                self.logger.error(f"Error during post monitoring: {str(e)}")
                time.sleep(self.config.ERROR_RETRY_DELAY)
                
    def run(self):
        """Main bot execution loop."""
        self.logger.info("Starting AutomodLoverBot...")
        
        try:
            while True:
                # Get the newest post
                newest_post = self.get_newest_post()
                
                if newest_post:
                    # If this is a different post, clear replied comments and update current post
                    if self.current_post_id != newest_post.id:
                        self.current_post_id = newest_post.id
                        self.replied_comments.clear()
                        self.logger.info(f"Switched to monitoring new post: {newest_post.id}")
                        
                    # Monitor the current post
                    newer_post = self.monitor_post(newest_post)
                    if newer_post:
                        newest_post = newer_post
                        continue
                        
                else:
                    self.logger.warning("No posts found, waiting before retry...")
                    time.sleep(self.config.ERROR_RETRY_DELAY)
                    
        except KeyboardInterrupt:
            self.logger.info("Bot execution stopped by user")
        except Exception as e:
            self.logger.error(f"Fatal error in bot execution: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        bot = AutomodLoverBot()
        bot.run()
    except Exception as e:
        print(f"Failed to start bot: {str(e)}")
        sys.exit(1)
