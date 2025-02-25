import unittest, sys
from unittest.mock import Mock
from dataclasses import dataclass
from typing import List
import helm_wrap
from hwrap_settings import REAL_HELM, HARBOR_HOST

class TestBuildCommand(unittest.TestCase):
 
    def setUp(self):
        helm_wrap.get_handles = Mock(return_value=['bitnami'])
        return super().setUp()
    

    def test_table_test(self):
        @dataclass
        class TestCase:
            name: str
            input: str
            expected: List[str]

        testcases = [
            TestCase(
                name = "version",
                input = "helm version",
                expected=[REAL_HELM, "version"],            
            ),
            TestCase(
                name = "install bitnami",
                input = "helm install test1 bitnami/mariadb",
                expected=[REAL_HELM, "install", "test1",
                         f"oci://{HARBOR_HOST}/bitnami/mariadb"
                    ],            
            ),
            TestCase(
                name = "install not bitnami",
                input = "helm install test2 salami/mariadb",
                expected=[REAL_HELM, "install", "test2",
                         "salami/mariadb"
                    ],            
            ),
            TestCase(
                name = "repo list",
                input = "helm repo list",
                expected=[REAL_HELM, "repo", "list",]
            ),

        ]

        for case in testcases:
            args = case.input.split()
            rslt = helm_wrap.build_command(args)
            returned = rslt.split()
            ndx = 0
            for val in case.expected:
                if val != "":
                    self.assertGreater(
                        len(returned),
                        ndx,
                        f"Case '{case.name}': returned {len(returned)} args, expected at least {len(case.expected)}",
                    )                        
                    self.assertEqual(returned[ndx], 
                                     val,
                                     f"Case '{case.name}', arg {ndx}: expected {case.expected[ndx]}, got {returned[ndx]}"
                    )
                ndx += 1


if __name__ == '__main__':
    unittest.main()
