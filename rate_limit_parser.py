"""
Rate limit parser module for handling Reddit API rate limit errors.
Parses error messages to extract wait times and convert to seconds.
"""

import re
import logging

class RateLimitParser:
    """Parser for Reddit API rate limit error messages."""
    
    def __init__(self):
        self.logger = logging.getLogger('RateLimitParser')
        
        # Regex patterns for different rate limit error formats
        self.patterns = [
            # "you are doing that too much. try again in 9 minutes."
            r'try again in (\d+) minute[s]?',
            # "you are doing that too much. try again in 30 seconds."
            r'try again in (\d+) second[s]?',
            # "you are doing that too much. try again in 1 hour."
            r'try again in (\d+) hour[s]?',
            # "Take a break for 9 minutes before trying again."
            r'take a break for (\d+) minute[s]?',
            r'take a break for (\d+) second[s]?', 
            r'take a break for (\d+) hour[s]?',
            # Alternative formats
            r'wait (\d+) minute[s]?',
            r'wait (\d+) second[s]?',
            r'wait (\d+) hour[s]?',
            # Generic "X minutes" format
            r'(\d+) minute[s]?',
            r'(\d+) second[s]?',
            r'(\d+) hour[s]?'
        ]
        
    def parse_rate_limit_error(self, error_message):
        """
        Parse a rate limit error message to extract wait time in seconds.
        
        Args:
            error_message (str): The error message from Reddit API
            
        Returns:
            int: Wait time in seconds, or 0 if no rate limit detected
        """
        if not error_message:
            return 0
            
        error_lower = error_message.lower()
        
        # Check if this is a rate limit error
        rate_limit_indicators = [
            'doing that too much',
            'try again in',
            'take a break for',
            'rate limit',
            'wait'
        ]
        
        is_rate_limit = any(indicator in error_lower for indicator in rate_limit_indicators)
        if not is_rate_limit:
            return 0
            
        self.logger.info(f"Detected rate limit error: {error_message}")
        
        # Try to extract time from the error message
        for pattern in self.patterns:
            match = re.search(pattern, error_lower)
            if match:
                time_value = int(match.group(1))
                
                if 'minute' in pattern:
                    wait_seconds = time_value * 60
                    self.logger.info(f"Parsed {time_value} minutes = {wait_seconds} seconds")
                    return wait_seconds
                elif 'hour' in pattern:
                    wait_seconds = time_value * 3600
                    self.logger.info(f"Parsed {time_value} hours = {wait_seconds} seconds")
                    return wait_seconds
                elif 'second' in pattern:
                    self.logger.info(f"Parsed {time_value} seconds")
                    return time_value
                    
        # If we detected a rate limit but couldn't parse the time, use default
        default_wait = 300  # 5 minutes default
        self.logger.warning(f"Could not parse wait time from rate limit message, using default {default_wait} seconds")
        return default_wait
        
    def convert_to_seconds(self, time_value, unit):
        """
        Convert time value to seconds based on unit.
        
        Args:
            time_value (int): The numeric time value
            unit (str): Time unit ('seconds', 'minutes', 'hours')
            
        Returns:
            int: Time in seconds
        """
        unit_multipliers = {
            'second': 1,
            'seconds': 1,
            'minute': 60,
            'minutes': 60,
            'hour': 3600,
            'hours': 3600
        }
        
        multiplier = unit_multipliers.get(unit.lower(), 1)
        return time_value * multiplier
