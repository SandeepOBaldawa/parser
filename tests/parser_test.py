import unittest
from src.parser import parseTransformQuery
DDOGQL_INPUT_FILE = "./input_ddogql_test.txt"
DDOGQL_OUTPUT_FILE = "./output_promql_test.txt"



class SumTestCase(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(
            parseTransformQuery(
                "sum:gcp.pubsub.subscription.oldest_unacked_message_age{subscription_id:redwood-resourcepool-worker-sub-xpress-lowpri-staging}"),
                "sum(gcp_pubsub_subscription_oldest_unacked_message_age{subscription_id=\"redwood-resourcepool-worker-sub-xpress-lowpri-staging\"})",
            'Wrong PromQL')

# Test everything
class SumTestCaseAll(unittest.TestCase):
    def test_all(self):
        try:
            with open(DDOGQL_INPUT_FILE, "r") as input_file, open(DDOGQL_OUTPUT_FILE, "r") as output_file:
                input_file_lines = input_file.readlines()
                output_file_lines = output_file.readlines()

                line_index = 0
                while(line_index < len(input_file_lines)):
                    self.assertEqual(
                        parseTransformQuery(input_file_lines[line_index]),
                        output_file_lines[line_index],
                        'Wrong PromQL'
                    )
                    line_index += 1

        except FileNotFoundError:
            msg = "Sorry, the file "+ DDOGQL_INPUT_FILE + "does not exist."
            print(msg)
