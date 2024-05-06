class Reimbursement:
    def __init__(self):
        self.ads = {
            '0011': [],
            '1011': [],
            '1111': [],
            '1010': []
        }
        self.ad_info = {
            '0011': {'cost_share_rate': 0.50, 'allowed_spend_per_ad': (0, 200)},
            '1011': {'cost_share_rate': 1.00, 'allowed_spend_per_ad': (1000, 2000)},
            '1111': {'cost_share_rate': 0.75, 'allowed_spend_per_ad': (0, 500)},
            '1010': {'cost_share_rate': 0.90, 'allowed_spend_per_ad': (0, 750)}
        }

    def add_ad(self, ad_type, spend):
        if ad_type in self.ads:
            allowed_spend = self.ad_info[ad_type]['allowed_spend_per_ad']
            if isinstance(allowed_spend, tuple):
                min_spend, max_spend = allowed_spend
                if min_spend <= spend <= max_spend:
                    self.ads[ad_type].append({'actual_spend': spend})
                else:
                    print("Spend amount is not within the allowed range.")

    def remove_ad(self, ad_type):
        if ad_type in self.ads and self.ads[ad_type]:
            self.ads[ad_type] = []

    def print_ads(self):
        for ad_type, ad_list in self.ads.items():
            for index, ad_info in enumerate(ad_list):
                print(f"Ad Type: {ad_type}, Cost Share Rate: {self.ad_info[ad_type]['cost_share_rate']}, "
                      f"Allowed Spend per Ad: {self.ad_info[ad_type]['allowed_spend_per_ad']}, Actual Spend: {ad_info['actual_spend']}")

    def total_reimbursement(self):
        total = 0
        for ad_type,ad_list in self.ads.items():
            for ad_info in ad_list:
                total += self.ad_info[ad_type]['cost_share_rate'] * ad_info['actual_spend']
        return total


# Unit testing
reimbursement = Reimbursement()
reimbursement.add_ad('0011', 150)
reimbursement.add_ad('0011', 70)
reimbursement.add_ad('1011', 1800)
reimbursement.add_ad('1111', 400)
reimbursement.add_ad('1010', 700)
reimbursement.add_ad('1010', 800)  # This should not be added because it exceeds the allowed spend
reimbursement.remove_ad('0011')
reimbursement.print_ads()
print("Total reimbursement:", reimbursement.total_reimbursement())