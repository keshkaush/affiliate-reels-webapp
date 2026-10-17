"""
Auto DM Responder
=================

Automatically sends affiliate links in DMs to EVERYONE who comments on posts.

This is the core monetization feature - when someone comments, they get
a DM with the affiliate link automatically.
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List


class AutoDMResponder:
    """
    Automatically sends affiliate links to all users who comment on posts.

    This runs continuously and monitors all your posts for new comments,
    then sends personalized DMs with affiliate links.
    """

    def __init__(self, config=None):
        self.config = config or {}
        self.processed_comments = set()  # Track which comments we've responded to
        self.rate_limit_delay = 2  # Seconds between DMs to avoid spam detection

    def monitor_and_respond(
        self,
        platform: str = 'instagram',
        check_interval_seconds: int = 60
    ):
        """
        Continuously monitor posts and auto-respond to ALL comments with DMs.

        Args:
            platform: Platform to monitor ('instagram', 'tiktok', 'facebook')
            check_interval_seconds: How often to check for new comments

        This runs forever until stopped.
        """
        print(f"🤖 Auto-DM Responder started for {platform}")
        print(f"   Checking every {check_interval_seconds} seconds")
        print(f"   ALL commenters will receive affiliate links via DM\n")

        while True:
            try:
                # Get all your recent posts
                recent_posts = self._get_recent_posts(platform, hours=24)

                for post in recent_posts:
                    # Get all comments on this post
                    comments = self._get_post_comments(post['id'], platform)

                    # Get the affiliate link for this post's product
                    affiliate_link = self._get_post_affiliate_link(post['id'])

                    if not affiliate_link:
                        print(f"⚠️  No affiliate link found for post {post['id']}, skipping")
                        continue

                    # Send DM to EVERY commenter
                    for comment in comments:
                        comment_id = f"{post['id']}_{comment['id']}"

                        # Skip if we already sent DM to this comment
                        if comment_id in self.processed_comments:
                            continue

                        # Send the DM with affiliate link
                        success = self._send_affiliate_dm(
                            user_id=comment['user_id'],
                            username=comment['username'],
                            affiliate_link=affiliate_link,
                            product_name=post.get('product_name', 'this product'),
                            platform=platform
                        )

                        if success:
                            print(f"✅ Sent affiliate link to @{comment['username']}")
                            self.processed_comments.add(comment_id)
                        else:
                            print(f"❌ Failed to send DM to @{comment['username']}")

                        # Rate limiting to avoid being flagged as spam
                        time.sleep(self.rate_limit_delay)

                # Wait before next check
                time.sleep(check_interval_seconds)

            except KeyboardInterrupt:
                print("\n🛑 Auto-DM Responder stopped by user")
                break

            except Exception as e:
                print(f"❌ Error in auto-responder: {e}")
                time.sleep(check_interval_seconds)

    def _send_affiliate_dm(
        self,
        user_id: str,
        username: str,
        affiliate_link: str,
        product_name: str,
        platform: str
    ) -> bool:
        """
        Send a personalized DM with the affiliate link.

        Returns:
            True if sent successfully, False otherwise
        """
        # Generate personalized message
        message = self._generate_dm_message(username, product_name, affiliate_link)

        try:
            # Send via platform API
            if platform == 'instagram':
                return self._send_instagram_dm(user_id, message)
            elif platform == 'facebook':
                return self._send_facebook_dm(user_id, message)
            else:
                return False

        except Exception as e:
            print(f"Error sending DM: {e}")
            return False

    def _generate_dm_message(
        self,
        username: str,
        product_name: str,
        affiliate_link: str
    ) -> str:
        """
        Generate a personalized DM message with the affiliate link.

        Templates rotate to avoid looking like spam.
        """
        templates = [
            f"Hey {username}! 👋 Thanks for commenting! Here's the link for {product_name}: {affiliate_link} #ad",

            f"Hi {username}! 😊 I saw you're interested in {product_name}! Here's where you can get it: {affiliate_link} (affiliate link)",

            f"{username} here's the link you asked about! 🔗 {affiliate_link}\n\nNote: This is an affiliate link, I earn a small commission if you purchase. Thanks for your support! 💙",

            f"Thanks for the comment {username}! 🙏 Get {product_name} here: {affiliate_link}\n\n(Disclosure: Affiliate link - I may earn from purchases) #ad",
        ]

        # Rotate through templates based on current time
        index = int(time.time()) % len(templates)
        return templates[index]

    def _get_recent_posts(self, platform: str, hours: int = 24) -> List[Dict]:
        """Get your recent posts from the last N hours."""
        # In production, use platform APIs:
        # - Instagram: Graph API /me/media
        # - TikTok: TikTok API /user/videos
        # - Facebook: Graph API /me/posts

        # Mock data for demo
        return [
            {
                'id': 'post_123',
                'product_name': 'Wireless Earbuds',
                'platform': platform,
                'created_at': datetime.now() - timedelta(hours=2)
            }
        ]

    def _get_post_comments(self, post_id: str, platform: str) -> List[Dict]:
        """Get all comments on a specific post."""
        # In production, use platform APIs:
        # - Instagram: Graph API /{media-id}/comments
        # - TikTok: TikTok API /video/comments
        # - Facebook: Graph API /{post-id}/comments

        # Mock data for demo
        return [
            {
                'id': 'comment_1',
                'user_id': 'user_123',
                'username': 'john_doe',
                'text': 'Love this!',
                'created_at': datetime.now()
            }
        ]

    def _get_post_affiliate_link(self, post_id: str) -> str:
        """Get the affiliate link associated with a post."""
        # In production, query your database
        # This should return the affiliate link you stored when posting

        # Mock data for demo
        return "https://amzn.to/example-affiliate-link"

    def _send_instagram_dm(self, user_id: str, message: str) -> bool:
        """Send DM via Instagram Graph API."""
        # Production implementation:
        # POST https://graph.instagram.com/v18.0/me/messages
        # with recipient user_id and message text

        print(f"[Instagram] Sending DM: {message[:50]}...")
        return True  # Mock success

    def _send_facebook_dm(self, user_id: str, message: str) -> bool:
        """Send DM via Facebook Messenger API."""
        # Production implementation:
        # POST to Facebook Messenger Send API

        print(f"[Facebook] Sending DM: {message[:50]}...")
        return True  # Mock success


__all__ = ['AutoDMResponder']
