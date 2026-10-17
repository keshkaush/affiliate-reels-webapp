"""
DM Handler Module
=================

Manages direct message interactions for affiliate link distribution.

Usage:
    from dm_handler import DMHandler

    handler = DMHandler()
    handler.respond_to_interest(user_id='user123', product_name='wireless earbuds')
"""

from .message_detector import MessageDetector
from .response_generator import ResponseGenerator
from .link_sender import LinkSender
from .auto_responder import AutoDMResponder


class DMHandler:
    """Main class for handling DM-based affiliate link sharing."""

    def __init__(self, config=None):
        self.detector = MessageDetector()
        self.response_gen = ResponseGenerator()
        self.link_sender = LinkSender(config)
        self.auto_responder = AutoDMResponder(config)

    def monitor_comments(self, post_id: str, platform: str = 'instagram'):
        """
        Monitor comments on a post for purchase interest signals.

        Args:
            post_id: ID of the post to monitor
            platform: Platform where post was made

        Returns:
            List of users showing interest
        """
        interested_users = []

        # Fetch comments
        comments = self._get_comments(post_id, platform)

        for comment in comments:
            # Detect purchase intent keywords
            has_interest = self.detector.detect_interest(comment['text'])

            if has_interest:
                interested_users.append({
                    'user_id': comment['user_id'],
                    'username': comment['username'],
                    'comment_text': comment['text'],
                    'interest_level': has_interest['confidence'],
                    'product_keywords': has_interest['detected_products']
                })

        return interested_users

    def send_product_inquiry(self, user_id: str, platform: str = 'instagram'):
        """
        Send an initial DM asking which product the user is interested in.

        Args:
            user_id: User to message
            platform: Platform to send DM on

        Returns:
            Message sent confirmation
        """
        message = self.response_gen.generate_inquiry()

        return self.link_sender.send_dm(
            user_id=user_id,
            platform=platform,
            message=message
        )

    def respond_with_link(
        self,
        user_id: str,
        product_name: str,
        affiliate_link: str,
        platform: str = 'instagram'
    ):
        """
        Send affiliate link in response to user inquiry.

        Args:
            user_id: User requesting the link
            product_name: Product they're interested in
            affiliate_link: Affiliate link to send
            platform: Platform to send on

        Returns:
            Message sent confirmation
        """
        # Generate personalized response
        message = self.response_gen.generate_link_response(
            product_name=product_name,
            affiliate_link=affiliate_link
        )

        return self.link_sender.send_dm(
            user_id=user_id,
            platform=platform,
            message=message
        )

    def auto_respond_to_dms(self, platform: str = 'instagram'):
        """
        Automatically respond to incoming DMs with affiliate links.

        This monitors your DM inbox and responds when users reply
        with product names from your posts.

        Args:
            platform: Platform to monitor

        Returns:
            Number of DMs responded to
        """
        pending_messages = self._get_pending_dms(platform)
        responses_sent = 0

        for dm in pending_messages:
            # Parse product request
            product_request = self.detector.extract_product_name(dm['text'])

            if product_request:
                # Look up affiliate link for this product
                affiliate_link = self._get_affiliate_link_for_product(
                    product_request['product_name']
                )

                if affiliate_link:
                    # Send link
                    self.respond_with_link(
                        user_id=dm['user_id'],
                        product_name=product_request['product_name'],
                        affiliate_link=affiliate_link,
                        platform=platform
                    )
                    responses_sent += 1

        return responses_sent

    def _get_comments(self, post_id: str, platform: str) -> list:
        """Fetch comments from a post."""
        # In production, use platform APIs
        # Meta Graph API for Instagram
        # TikTok API for TikTok
        return []

    def _get_pending_dms(self, platform: str) -> list:
        """Fetch pending DMs from platform."""
        # Use platform messaging APIs
        return []

    def _get_affiliate_link_for_product(self, product_name: str) -> str:
        """Look up stored affiliate link for a product."""
        # Query database for product's affiliate link
        return None

    def start_auto_dm_responder(self, platform: str = 'instagram', check_interval: int = 60):
        """
        Start the automatic DM responder that sends affiliate links to ALL commenters.

        This is the key feature - every person who comments gets a DM with the link.

        Args:
            platform: Platform to monitor ('instagram', 'tiktok', 'facebook')
            check_interval: How often to check for new comments (seconds)
        """
        print(f"\n🚀 Starting Auto-DM Responder")
        print(f"   Platform: {platform}")
        print(f"   Check interval: {check_interval}s")
        print(f"   Mode: Send affiliate link to EVERY commenter\n")

        self.auto_responder.monitor_and_respond(
            platform=platform,
            check_interval_seconds=check_interval
        )


__all__ = ['DMHandler']
