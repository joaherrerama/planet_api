import unittest
import sys

sys.path.append("..")
from planet_cli_tool.main import main


class test_sim_model(unittest.TestCase):
    def setUp(self):
        self.api_key = ""
        self.wrong_api_key = ""
        self.aoi = ""
        self.aoi_multipolygon = ""
        self.aoi_invalid = ""
        self.toi = ""
        self.toi_single_date = ""
        self.toi_range = ""
        self.toi_range_invalid = ""

    def test_error_no_arg(self):
        main([])
        self.assertEqual("No args provided -  Default Values will be executed")


if __name__ == "__main__":
    unittest.main()
