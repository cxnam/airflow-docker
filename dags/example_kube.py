from airflow.utils.dates import days_ago
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.models import DAG
from datetime import datetime, timedelta
#from airflow.contrib.kubernetes.volume_mount import VolumeMount  # noqa
#from airflow.contrib.kubernetes.volume import Volume 

log = LoggingMixin().log

try:
    # Kubernetes is optional, so not available in vanilla Airflow
    # pip install apache-airflow[kubernetes]
    from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

    args = {
        'owner': 'airflow',
        'start_date': days_ago(2),
        'retries': 1,
        'retry_delay': timedelta(minutes=2)
    }

    dag = DAG(
        dag_id='example_data_usage_kube',
        default_args=args,
        schedule_interval=None)

    tolerations = [
        {
            'key': "dedicated",
            'operator': 'Equal',
            'value': 'true'
        }
    ]

    example_data_usage = KubernetesPodOperator(
        namespace='airflow',
        image="namcx/data-usage",
        #env_vars={"ARGS": ""},
        name="example_data_usage-pod",
        in_cluster=True,
        task_id="example_data_usage",
        get_logs=True,
        dag=dag,
        is_delete_operator_pod=False,
        tolerations=tolerations
    )

    # construct dependencies
    #[stgstate, stgcustomers] >> aggcustomers >> extractcustomers
except ImportError as e:
    log.warn("Could not import KubernetesPodOperator: " + str(e))
    log.warn("Install kubernetes dependencies with: "
             "    pip install apache-airflow[kubernetes]")