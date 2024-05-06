from django.db import models
from django.utils import timezone

class InvalidSpendException(Exception):
    pass
class Ad(models.Model):
    ad_type = models.CharField(max_length=10)
    actual_spend = models.FloatField()
    count = models.IntegerField()
    date = models.DateField(default=timezone.now)
class Reimbursement:
    ad_info = {
        '0011': {'cost_share_rate': 0.50, 'allowed_spend_per_ad': (0, 200)},
        '1011': {'cost_share_rate': 1.00, 'allowed_spend_per_ad': (1000, 2000)},
        '1111': {'cost_share_rate': 0.75, 'allowed_spend_per_ad': (0, 500)},
        '1010': {'cost_share_rate': 0.90, 'allowed_spend_per_ad': (0, 750)}
    }

    def add_ad(self, ad_type, count, spend):

        if count == 0:
            raise InvalidSpendException("Please input count")

        if ad_type in self.ad_info:
            allowed_spend = self.ad_info[ad_type]['allowed_spend_per_ad']
            if isinstance(allowed_spend, tuple):
                min_spend, max_spend = allowed_spend
                if min_spend <= spend <= max_spend:
                    Ad.objects.create(ad_type=ad_type, actual_spend=spend, count=count)
                else:
                    raise InvalidSpendException("Spend amount is not within the allowed range.")

    def get_ads(self):
        ads_data = []
        for ad in Ad.objects.all():
            ads_data.append({
                'id': ad.id,
                'ad_type': ad.ad_type,
                'count': ad.count,
                'date': ad.date,
                'actual_spend': ad.actual_spend,
                'cost_share': self.ad_info[ad.ad_type]['cost_share_rate'] * ad.actual_spend,
                'reimbursement': self.ad_info[ad.ad_type]['cost_share_rate'] * ad.actual_spend * ad.count
            })
        return ads_data

    def remove_ad(self, ad_id):
        try:
            ad = Ad.objects.get(pk=ad_id)
            ad.delete()
        except Ad.DoesNotExist:
            raise InvalidSpendException("Ad does not exist.")