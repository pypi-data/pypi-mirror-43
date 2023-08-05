import time

from google.protobuf.timestamp_pb2 import Timestamp

from custom_metrics.helpers.stackdriver_metrics import create_descriptor, log_point
from datetime import datetime
from airflow.plugins_manager import AirflowPlugin


TASK_DURATION_METRIC_TYPE = 'custom.googleapis.com/airflow/extensions/task_duration/1.2'

def monitor(operator_class, **kwargs):

    google_project_name = kwargs.pop('google_project')
    google_location = kwargs.pop('google_location')
    labels = kwargs.pop('labels', [])

    class MonitoredOperator(operator_class):
        def __init__(self, **kwargs):
            super(MonitoredOperator, self).__init__(**kwargs)

            self.google_project_name = google_project_name
            self.google_location = google_location
            self.labels = labels

            # Make sure we have required kwargs
            if self.google_project_name is None or self.google_location is None:
                raise Exception('Both google_project and google_location need to be provided in the monitored '
                                'operator keyword arguments.')

            # Confirm that if labels are provided, each dictionary in the list has the right structure
            if len(self.labels) != 0:
                for label in self.labels:
                    if type(label) is not dict:
                        raise Exception('Elements in the labels list need to be dictionaries.')
                    for required_key in ['key', 'value', 'description', 'value_type']:
                        if required_key not in label.keys():
                            raise Exception(
                                'The key ' + required_key + ' is not in the provided labels dictionary:\n' + str(label))

        def execute(self, context):
            start_time = datetime.now()
            return_val = super(MonitoredOperator, self).execute(context)
            end_time = datetime.now()

            delta = (end_time - start_time).microseconds

            dag_task_key = '__'.join(context.get('task_instance_key_str').split('__')[:2])
            metric_dict = get_total_time_dict_from_context(context, self.google_project_name, dag_task_key,
                                                           label_list=self.get_labels_for_metric())
            point_dict = get_point_dict_from_context(context, self.google_location, delta, dag_task_key,
                                                     label_values=self.get_labels_for_point())

            try:
                metric_output = create_descriptor(metric_dict, self.google_project_name)
                self.log.info(metric_output)
            except:
                self.log.warning(
                    'Metric description could not be created in ' + self.google_project_name + '\n' + str(point_dict))

            try:
                point_output = log_point(point_dict, self.google_project_name)
                self.log.info(point_output)

            except:
                self.log.warning('Point could not be logged to ' + self.google_project_name + '\n' + str(point_dict))

            return return_val

        def get_labels_for_metric(self):
            """
            Example:
            [
                {
                    "key": "run_id",
                    "value_type": "STRING",
                    "description": "The ID of the DAG run."
                }
            ]
            """
            if len(self.labels) == 0:
                return None

            return [{k: label_dict.get(k) for k in ['key', 'value_type', 'description']} for label_dict in self.labels]

        def get_labels_for_point(self):
            """
            :return: Dictionary with label key and value for each label
            Example:
                {
                    "run_id": "012345"
                }
            """
            if len(self.labels) == 0:
                return None

            return {label_dict.get('key'): label_dict.get('value') for label_dict in self.labels}

    MonitoredOperator.__name__ = operator_class.__name__
    return MonitoredOperator(**kwargs)


def monitor_operator(operator_instance, google_project_name, google_location):
    operator_instance.original_execute = operator_instance.execute
    operator_instance.execute = lambda context=None: wrapped_execute(operator_instance, context, google_project_name,
                                                                     google_location)
    return operator_instance


def wrapped_execute(instance, context, google_project_name, google_location):
    start_time = datetime.now()
    instance.original_execute(context)
    end_time = datetime.now()

    delta = (end_time - start_time).microseconds

    # The metric should be specific to the dag and task but not run
    dag_task_key = '__'.join(context.get('task_instance_key_str').split('__')[:2])
    metric_dict = get_total_time_dict_from_context(context, google_project_name, dag_task_key)
    point_dict = get_point_dict_from_context(context, google_location, delta, dag_task_key)

    try:
        metric_output = create_descriptor(metric_dict, google_project_name)
        instance.log.info(metric_output)
    except:
        instance.log.warning(
            'Metric description could not be created in ' + google_project_name + '\n' + str(point_dict))


    try:
        point_output = log_point(point_dict, google_project_name)
        instance.log.info(point_output)

    except:
        instance.log.warning('Point could not be logged to ' + google_project_name + '\n' + str(point_dict))


def get_total_time_dict_from_context(context, google_project_name, task_key, label_list=None):
    return {
        "name": "projects/" + google_project_name,
        "description": "Task Duration",
        "display_name": task_key,
        "type": TASK_DURATION_METRIC_TYPE,
        "metric_kind": "GAUGE",
        "value_type": "INT64",
        "labels": label_list if label_list is not None else [],
    }


def get_point_dict_from_context(context, google_location, time_delta, task_key, label_values=None):
    now = time.time()

    return {
        "metric": {
            "type": TASK_DURATION_METRIC_TYPE,
            "labels": label_values if label_values is not None else {},
        },
        "resource": {
            "type": "generic_task",
            "labels": {
                "job": "extensions",
                "location": google_location,
                "namespace": task_key,
                "task_id": "log_duration"
            }
        },
        "metadata": {},
        "metric_kind": "GAUGE",
        "value_type": "INT64",
        "points": [
            {
                "interval": {
                    "start_time": Timestamp(seconds=int(now), nanos=int((now - int(now)) * 10 ** 9)),
                    "end_time": Timestamp(seconds=int(now), nanos=int((now - int(now)) * 10 ** 9))
                },
                "value": {
                    "int64_value": time_delta
                }
            }
        ]
    }


class AirflowMetricPlugin(AirflowPlugin):
    name = "monitor_test"
    macros = [monitor_operator, monitor]
