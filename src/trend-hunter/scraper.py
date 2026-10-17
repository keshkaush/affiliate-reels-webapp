"""
Social Platform Scraper Module
===============================

Handles scraping and content retrieval from TikTok, Instagram,
and YouTube for trending product reels.
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional


class SocialScraper:
    """
    Multi-platform social media scraper for finding trending product reels.
    """

    def __init__(self):
        self.platforms = {
            'instagram': {'url': 'https://www.instagram.com', 'rate_limit': 5},
            'facebook': {'url': 'https://www.facebook.com', 'rate_limit': 5},
            'youtube': {'url': 'https://www.youtube.com', 'rate_limit': 3}
        }

    def scrape_platform(
        self,
        niche: str = None,
        platform: str = None,
        keywords: List[str] = None
    ) -> List[Dict]:
        """
        Scrape a specific platform for trending content.

        Args:
            niche: Content category (gadgets/accessories/clothing/lifestyle)
            platform: Target platform ('tiktok', 'instagram', 'youtube')
            keywords: Search keywords to filter results

        Returns:
            List of video data dictionaries
        """
        if not platform:
            platform = 'instagram'  # Default

        if not niche:
            niche = 'all'

        videos = []

        try:
            # Get trending videos from platform
            trend_videos = self._get_trending(platform)

            for video in trend_videos:
                # Check if matches niche/keywords
                if self._matches_niche(video, niche, keywords):
                    video_data = {
                        'platform': platform,
                        'video_url': video['url'],
                        'title': video.get('title', ''),
                        'author': video.get('author', ''),
                        'views': video.get('views', 0),
                        'likes': video.get('likes', 0),
                        'shares': video.get('shares', 0),
                        'comments': video.get('comments', 0),
                        'timestamp': datetime.now().isoformat(),
                        'niche': niche,
                        'keywords_matched': [k for k in keywords if k.lower() in video['title'].lower()]
                    }

                    videos.append(video_data)

        except Exception as e:
            print(f"Error scraping {platform}: {e}")

        return videos

    def _get_trending(self, platform: str) -> List[Dict]:
        """Get trending videos from a platform."""
        # Note: In production, use official APIs or proxy services
        # This is simplified for demo purposes
        return [
            {
                'url': f'https://www.instagram.com/reel/{i}' if platform == 'instagram' else f'https://www.facebook.com/watch/?v={i}',
                'title': f'Viral Product Content #{i}',
                'author': f'user_{i}',
                'views': 100000 + i * 500,
                'likes': 5000 + i * 200,
                'shares': 1000 + i * 50,
                'comments': 200 + i * 10
            } for i in range(1, 6)
        ]

    def _matches_niche(
        self,
        video: Dict,
        niche: str,
        keywords: Optional[List[str]] = None
    ) -> bool:
        """Check if a video matches the target niche."""
        title_lower = video.get('title', '').lower()

        niche_keywords = {
            'gadgets': ['tech', 'gadget', 'device', 'smart', 'wearable'],
            'accessories': ['jewelry', 'watch', 'bag', 'case', 'earrings'],
            'clothing': ['outfit', 'fashion', 'dress', 'shirt', 'pants'],
            'lifestyle': ['home', 'living', 'routine', 'productivity', 'minimalist']
        }

        if niche == 'all':
            return keywords is None or keywords  # Accept all if no niche filter

        niche_words = niche_keywords.get(niche, [])
        matches = [kw for kw in niche_words if kw in title_lower]

        if keywords:
            keyword_matches = [k for k in keywords if k.lower() in title_lower]
            return len(matches) > 0 or len(keyword_matches) > 0

        return len(matches) > 0


__all__ = ['SocialScraper']
