"""
Affiliate Manager Module
========================

Matches discovered products to affiliate programs and manages affiliate links.

Usage:
    from affiliate_manager import AffiliateManager

    manager = AffiliateManager()
    links = manager.find_affiliate_links(product_name='wireless earbuds')
"""

from .partner_finder import PartnerFinder
from .link_generator import LinkGenerator
from .commission_tracker import CommissionTracker


class AffiliateManager:
    """Main class for managing affiliate partnerships and links."""

    def __init__(self, config=None):
        self.partner_finder = PartnerFinder(config)
        self.link_generator = LinkGenerator(config)
        self.commission_tracker = CommissionTracker(config)

        # Supported affiliate networks
        self.networks = [
            'amazon',          # Amazon Associates
            'flipkart',        # Flipkart Affiliate (India)
            'shareasale',      # ShareASale
            'cj',              # CJ Affiliate (Commission Junction)
            'impact',          # Impact Radius
            'clickbank',       # ClickBank (digital products)
        ]

    def find_affiliate_links(self, product_name: str, product_url: str = None) -> list:
        """
        Find affiliate programs for a given product.

        Args:
            product_name: Name or description of the product
            product_url: Optional direct URL to the product

        Returns:
            List of affiliate link options with commission rates
        """
        # Search across all networks
        affiliate_options = []

        for network in self.networks:
            try:
                results = self.partner_finder.search_network(
                    network=network,
                    product=product_name,
                    url=product_url
                )

                for result in results:
                    affiliate_link = self.link_generator.generate(
                        network=network,
                        product_url=result['url'],
                        affiliate_id=result.get('affiliate_id')
                    )

                    affiliate_options.append({
                        'network': network,
                        'product_name': result['name'],
                        'affiliate_link': affiliate_link,
                        'commission_rate': result.get('commission_rate', 'Unknown'),
                        'cookie_duration': result.get('cookie_days', 30),
                        'priority_score': self._calculate_priority(result)
                    })

            except Exception as e:
                print(f"Error searching {network}: {e}")
                continue

        # Sort by priority score (highest commission + best terms)
        affiliate_options.sort(key=lambda x: x['priority_score'], reverse=True)

        return affiliate_options

    def _calculate_priority(self, affiliate_data: dict) -> float:
        """
        Calculate priority score for an affiliate program.

        Higher score = better affiliate opportunity
        """
        commission = float(affiliate_data.get('commission_rate', 5))  # Default 5%
        cookie_days = int(affiliate_data.get('cookie_days', 30))
        conversion_rate = float(affiliate_data.get('conversion_rate', 2.0))  # Default 2%

        # Weighted scoring
        score = (
            commission * 0.4 +           # Commission rate weight
            (cookie_days / 30) * 0.2 +   # Cookie duration weight (normalized to 30 days)
            conversion_rate * 0.3 +      # Conversion rate weight
            0.1                          # Base score
        )

        return round(score, 2)

    def get_best_link(self, product_name: str) -> dict:
        """Get the single best affiliate link for a product."""
        links = self.find_affiliate_links(product_name)

        if not links:
            return None

        return links[0]  # Already sorted by priority

    def track_click(self, affiliate_link: str, post_id: str = None):
        """Track when an affiliate link is shared."""
        self.commission_tracker.log_click(
            link=affiliate_link,
            post_id=post_id,
            timestamp=None  # Auto-timestamp
        )

    def get_earnings_report(self, days: int = 30) -> dict:
        """Get earnings report for the last N days."""
        return self.commission_tracker.get_report(days=days)


__all__ = ['AffiliateManager']
