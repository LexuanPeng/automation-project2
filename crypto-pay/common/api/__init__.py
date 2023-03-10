from .payment import StagingPayment
from .payment_ops import StagingPaymentOps
from .payout import StagingPayout
from .subscriptions import StagingSubscriptions
from .subscriptions_ops import StagingSubscriptionsOps
from .terms import StagingTerms
from .registration import StagingRegistration


class Apis:
    def __init__(self):
        self.payment = StagingPayment()
        self.payment_ops = StagingPaymentOps()
        self.payout = StagingPayout()
        self.subscriptions = StagingSubscriptions()
        self.subscriptions_ops = StagingSubscriptionsOps()
        self.terms = StagingTerms()
        self.registration = StagingRegistration()
