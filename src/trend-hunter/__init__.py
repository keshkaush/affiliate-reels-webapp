"""
TrendHunter Module
==================

Finds trending faceless product reels about gadgets, accessories,
clothing, and lifestyle items.

Usage:
    from trend_hunter import TrendHunter
    hunter = TrendHunter()

    trends = hunter.find_trending(niche='gadgets')
    for reel in trends:
        print(f"{reel['platform']}: {reel['video_url']}")
"""

from .scraper import SocialScraper
from .ai_analyzer import AIVisionAnalyzer
from .trends_collector import TrendsCollector


class TrendHunter:
    """Main class for discovering trending faceless product reels."""

    def __init__(self, api_keys=None):
        self.scraper = SocialScraper()
        self.ai_analyzer = AIVisionAnalyzer(api_keys=api_keys)
        self.collector = TrendsCollector()

        # Target niches
        self.niches = ['gadgets', 'accessories', 'clothing', 'lifestyle']

    def find_trending(self, niche: str = None, limit: int = 10, platform: str = None) -> list:
        """
        Find trending reels in a specific niche.

        Args:
            niche: One of ['gadgets', 'accessories', 'clothing', 'lifestyle']
            limit: Number of results to return
            platform: Filter by platform ('tiktok', 'instagram', 'youtube')

        Returns:
            List of trending video data with metadata
        """
        if not niche:
            niche = self.niches[0]  # Default to gadgets

        videos = []

        # Scrape across platforms
        for platform in ['instagram', 'facebook', 'youtube']:
            if platform and platform != platform.lower():
                continue

            platform_videos = self.scraper.scrape_platform(
                niche=niche,
                platform=platform,
                keywords=self._get_keywords(niche)
            )

            for video in platform_videos:
                # Analyze with AI
                analysis = self.ai_analyzer.analyze_video(video)

                if analysis.is_faceless and analysis.products_found:
                    video['ai_analysis'] = analysis
                    videos.append(video)

        # Sort by trend score
        videos.sort(key=lambda x: x.get('trend_score', 0), reverse=True)

        return videos[:limit]

    def _get_keywords(self, niche: str) -> list:
        """Get trending keywords for a niche."""
        keyword_map = {
            'gadgets': [
                'latest tech', 'new gadgets', 'must buy technology',
                'cool gadgets 2024', 'tech review', 'gadget hunt',
                'smart home', 'wearable tech', 'audio gear'
            ],
            'accessories': [
                'trending accessories', 'must have jewelry', 'bag collection',
                'watch collection', 'luxury accessories', 'fashion finds'
            ],
            'clothing': [
                'outfit ideas', 'street style', 'fashion haul',
                'thrift flip', 'sustainable fashion', 'capsule wardrobe'
            ],
            'lifestyle': [
                'minimalist living', 'productivity tips', 'home decor',
                'wellness routine', 'morning habits', 'organization hacks'
            ]
        }

        return keyword_map.get(niche, ['trending', 'viral', 'must see'])

    def search_by_product(self, product_keywords: str) -> list:
        """Search for reels featuring specific products."""
        videos = self.scraper.scrape_platform(
            niche='all',
            platform='instagram',  # Start with Instagram (highest engagement in India)
            keywords=product_keywords.split()
        )

        return [v for v in videos if self.ai_analyzer.has_products(v)]


__all__ = ['TrendHunter']
