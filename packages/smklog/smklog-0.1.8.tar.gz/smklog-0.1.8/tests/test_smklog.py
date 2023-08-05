import json
import unittest

from smklog import SmkLog


class TestSmkLog(unittest.TestCase):
    platform = "youzan"
    service = "nomad_envoy_order"
    maxDiff = None

    def test_smklog(self):
        logger = SmkLog(self.platform, self.service)

        source = "odoo"
        category = "info"
        label = "get_all_orders"

        message = "Translated error message for youzan service not responding"

        data = """{"key":"value","键":"值"}"""

        timing = """{"total":3}"""

        user = "1234567"

        store_id = "samarkand.youzan.foreveryoung"
        request_id = "0EFD81C9-16BF-4FF6-8CF8-00FEB0619A47"

        msg1 = logger.info(source, category, label, message, data, timing, user)
        self.assertTrue(isinstance(json.loads(msg1), dict),
                        "Message should be JSON format")
        self.assertEqual(json.loads(msg1)["data"], data,
                         "Chinese characters should keep original, not escaped")
        self.assertFalse("store_id" in json.loads(msg1),
                         "store_id is optional.")
        self.assertFalse("request_id" in json.loads(msg1),
                         "request_id is also optional")

        msg2 = logger.info(source, category, label, message, data, timing, user,
                           store_id, request_id)

        include_field_msg = "all fields should be included, including store_id and request_id."
        self.assertIn("store_id", json.loads(msg2), include_field_msg)
        self.assertIn("request_id", json.loads(msg2), include_field_msg)

        self.assertTrue("store_id" in json.loads(msg2),
                        "we passed store_id field")
        self.assertTrue("request_id" in json.loads(msg2),
                        "we passed request_id field")

        data_json = {"key": "value", "键": "值"}
        msg3 = logger.error(source, category, label, message, data_json,
                            timing, user, store_id, request_id)
        self.assertEqual(json.loads(msg3)["data"], {"key":"value","键":"值"},
                         "Chinese characters should keep original even when "
                         "data is JSON data format.")
