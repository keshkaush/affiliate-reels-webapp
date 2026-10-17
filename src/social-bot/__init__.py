"""
Social Bot Module
=================

Handles content posting automation across Instagram, TikTok, and Facebook.

Usage:
    from social_bot import SocialBot

    bot = SocialBot()
    bot.post_reel(video_path='./video.mp4', caption='Check this out!', platform='instagram')
"""

from .video_downloader import VideoDownloader
from .content_optimizer import ContentOptimizer
from .platform_poster import PlatformPoster
from .scheduler import PostScheduler


class SocialBot:
    """Main class for automating social media content posting."""

    def __init__(self, config=None):
        self.downloader = VideoDownloader()
        self.optimizer = ContentOptimizer()
        self.poster = PlatformPoster(config)
        self.scheduler = PostScheduler()

    def download_and_post(
        self,
        video_url: str,
        product_name: str,
        affiliate_link: str,
        platforms: list = None
    ) -> dict:
        """
        Download a trending reel and post it across platforms.

        Args:
            video_url: URL of the video to download
            product_name: Name of the product being promoted
            affiliate_link: Affiliate link to share
            platforms: List of platforms to post to ['instagram', 'tiktok', 'facebook']

        Returns:
            Dictionary with post results for each platform
        """
        if not platforms:
            platforms = ['instagram', 'facebook']

        # Step 1: Download video
        video_path = self.downloader.download(video_url)

        # Step 2: Optimize content (captions, hashtags, disclosure)
        optimized_content = self.optimizer.optimize(
            video_path=video_path,
            product_name=product_name,
            affiliate_link=affiliate_link
        )

        # Step 3: Post to each platform
        results = {}
        for platform in platforms:
            try:
                post_result = self.poster.post(
                    platform=platform,
                    video_path=optimized_content['video_path'],
                    caption=optimized_content['captions'][platform],
                    hashtags=optimized_content['hashtags'][platform]
                )

                results[platform] = {
                    'success': True,
                    'post_id': post_result['id'],
                    'post_url': post_result['url'],
                    'scheduled_time': post_result.get('scheduled_time')
                }

            except Exception as e:
                results[platform] = {
                    'success': False,
                    'error': str(e)
                }

        return results

    def schedule_post(
        self,
        video_url: str,
        product_name: str,
        affiliate_link: str,
        post_time: str,
        platforms: list = None
    ):
        """
        Schedule a post for later.

        Args:
            video_url: URL of video to post
            product_name: Product name
            affiliate_link: Affiliate link
            post_time: ISO timestamp for when to post
            platforms: Target platforms

        Returns:
            Scheduled post ID
        """
        return self.scheduler.schedule(
            video_url=video_url,
            product_name=product_name,
            affiliate_link=affiliate_link,
            post_time=post_time,
            platforms=platforms or ['instagram', 'facebook']
        )

    def get_post_performance(self, post_id: str, platform: str) -> dict:
        """Get engagement metrics for a posted reel."""
        return self.poster.get_metrics(
            post_id=post_id,
            platform=platform
        )


__all__ = ['SocialBot']
