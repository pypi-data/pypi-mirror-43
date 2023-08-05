from custom_metrics.helpers import get_total_time_dict_from_context, get_point_dict_from_context
from custom_metrics.helpers.stackdriver_metrics import create_descriptor, log_point
from datetime import datetime


def monitor(operator_class, **kwargs):
    # TODO: let's make monitor function accept a `metric_reporter`, which will handle logics performed in `get_labels_for_metric` and `get_labels_for_point`
    # TODO: as well as formatting inputs for Stackdriver and any other potential integrations (can be done with bunch of Handler classes that gets injected into the metric_reporter)
    google_project_name = kwargs.pop('google_project')
    google_location = kwargs.pop('google_location')
    labels = kwargs.pop('labels', [])

    # define arguments that need to be templated here
    fields_to_template = ['google_project_name', 'google_location', 'labels']

    class MonitoredOperator(operator_class):

        template_fields = list(operator_class.template_fields) + fields_to_template

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
            metric_dict = get_total_time_dict_from_context(self.google_project_name, dag_task_key,
                                                           label_list=self.get_labels_for_metric())
            point_dict = get_point_dict_from_context(self.google_location, delta, dag_task_key,
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

            labels = [{k: label_dict.get(k) for k in ['key', 'value_type', 'description']} for label_dict in self.labels]
            self.log.info('Metric labels retrieved:\n' + str(labels))
            return labels

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

            point_labels = {label_dict.get('key'): label_dict.get('value') for label_dict in self.labels}
            self.log.info('Point labels retrieved:\n' + str(point_labels))
            return point_labels

    MonitoredOperator.__name__ = operator_class.__name__
    return MonitoredOperator(**kwargs)
