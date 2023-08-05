#
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.
#

import unittest

import numpy as np

import kglib.kgcn.learn.metrics.report as metrics


class TestMetricsReport(unittest.TestCase):
    def test_print(self):
        y_true = np.array([0, 1, 2, 0])
        y_pred = y_true
        # expected_confusion_matrix = np.array([[2, 0, 0], [0, 1, 0], [0, 0, 1]])
        metrics.report_multiclass_metrics(y_true, y_pred)


if __name__ == "__main__":
    unittest.main()
