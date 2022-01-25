import unittest
from parser import parseTransformQuery
class SumTestCase(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(
            parseTransformQuery(
                "sum:gcp.pubsub.subscription.oldest_unacked_message_age{subscription_id:redwood-resourcepool-worker-sub-xpress-lowpri-staging}"),
                "sum(gcp_pubsub_subscription_oldest_unacked_message_age{subscription_id=\"redwood-resourcepool-worker-sub-xpress-lowpri-staging\"})",
            'Wrong PromQL')
