from django.db import models
from django.utils import timezone

class Reimbursement:
    def __init__(self):
        self.ads = {
            '0011': {'cost_share_rate': 0.50, 'allowed_spend_per_ad': 200, 'count': 0, 'date': None, 'actual_spend': 0.0},
            '1011': {'cost_share_rate': 1.00, 'allowed_spend_per_ad': (1000, 2000), 'count': 0, 'date': None, 'actual_spend': 0.0},
            '1111': {'cost_share_rate': 0.75, 'allowed_spend_per_ad': 500, 'count': 0, 'date': None, 'actual_spend': 0.0},
            '1010': {'cost_share_rate': 0.90, 'allowed_spend_per_ad': 750, 'count': 0, 'date': None, 'actual_spend': 0.0}
        }

    def add_ad(self, ad_type, count, spend):
        if ad_type in self.ads:
            if isinstance(self.ads[ad_type]['allowed_spend_per_ad'], tuple):
                min_spend, max_spend = self.ads[ad_type]['allowed_spend_per_ad']
                if min_spend <= spend <= max_spend:
                    self.ads[ad_type]['count'] += count
                    self.ads[ad_type]['actual_spend'] += spend
                    self.ads[ad_type]['date'] = timezone.now().date()

            elif isinstance(self.ads[ad_type]['allowed_spend_per_ad'], int):
                if spend <= self.ads[ad_type]['allowed_spend_per_ad']:
                    self.ads[ad_type]['count'] += count
                    self.ads[ad_type]['actual_spend'] += spend
                    self.ads[ad_type]['date'] = timezone.now().date()

    def remove_ad(self, ad_type):
        if ad_type in self.ads and self.ads[ad_type]['count'] > 0:
            self.ads[ad_type]['count'] -= 1

    def print_ads(self):
        for ad_type, ad_info in self.ads.items():
            print(f"Ad Type: {ad_type}, Count: {ad_info['count']}, Cost Share Rate: {ad_info['cost_share_rate']}, Allowed Spend per Ad: {ad_info['allowed_spend_per_ad']}")

    def total_reimbursement(self):
        total = 0
        for ad_type, ad_info in self.ads.items():
            if isinstance(ad_info['allowed_spend_per_ad'], tuple):
                min_spend, max_spend = ad_info['allowed_spend_per_ad']
                total += ad_info['count'] * ad_info['cost_share_rate'] * min_spend
            else:
                total += ad_info['count'] * ad_info['cost_share_rate'] * ad_info['allowed_spend_per_ad']
        return total