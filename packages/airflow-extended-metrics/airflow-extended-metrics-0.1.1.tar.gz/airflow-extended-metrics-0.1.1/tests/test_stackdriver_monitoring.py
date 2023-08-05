import time
from google.protobuf.timestamp_pb2 import Timestamp

from extended_metrics.helpers.stackdriver_metrics import create_descriptor, log_point

#####
# Test creating the metric descriptor
#####

example_desc_dict = {
        "name": "projects/nytdata",
        "description": "Number of Airflow DAG starts.",
        "display_name": "extensions start",
        "type": "custom.googleapis.com/extensions/dag_starts_0.1",
        "metric_kind": "CUMULATIVE",
        "value_type": "DOUBLE",
        "labels": [
            {
                "key": "run_id",
                "value_type": "STRING",
                "description": "The ID of the DAG run."
            },
        ],
    }

# Expected outcome: prints metric dict after creating metric
print(create_descriptor(example_desc_dict, 'nytdata'))

#####
# Test logging a point the the created metric
#####

now = time.time()
example_series_dict = {
        "metric": {
            "type": "custom.googleapis.com/extensions/dag_starts_0.1",
            "labels": {
                "run_id": "1234567890123456789"
            }
        },
        "resource": {
            "type": "generic_task",
            "labels": {
                "job": "extensions",
                "location": "us-central1",
                "namespace": "custom_logger",
                "task_id": "log_start"
            }
        },
        "metadata": {},
        "metric_kind": "CUMULATIVE",
        "value_type": "DOUBLE",
        "points": [
            {
                "interval": {
                    "start_time": Timestamp(seconds=int(now), nanos=int((now - int(now)) * 10**9)),
                    "end_time": Timestamp(seconds=int(now)+1, nanos=int((now - int(now)) * 10**9))
                },
                "value": {
                    "double_value": 1.0
                }
            }
        ]
    }

# Expected outcome: None is printed
print(log_point(example_series_dict, 'nytdata'))
