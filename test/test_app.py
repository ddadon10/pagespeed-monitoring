import unittest
import json
import os
from unittest.mock import MagicMock

from pagespeed_monitoring import app


package_directory = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(package_directory,'data/pagespeed_result.json'), 'r') as stream:
    pagespeed_result = json.load(stream)
app._get_result = MagicMock(return_value=pagespeed_result)


class TestPagespeedMonitoring(unittest.TestCase):

    def test_get_result(self):
        result = app.get_filtered_result({})
        self.assertEqual(result, pagespeed_result)


if __name__ == "__main__":
    unittest.main()
