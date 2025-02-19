import pytest
import os
from airflow.models import DagBag
from airflow.utils.dag_cycle_tester import check_cycle


@pytest.fixture()
def dagbag():
    current_path = os.path.dirname(os.path.abspath(__file__))
    parent_path = os.path.dirname(current_path)
    dags_path = os.path.join(parent_path, "dags")

    return DagBag(dag_folder=dags_path, include_examples=False)


def test_dag_loaded(dagbag):
    dag = dagbag.get_dag(dag_id="bq_ctas")
    assert dagbag.import_errors == {}
    assert dag is not None
    assert len(dag.tasks) == 1


def test_dag_cycles(dagbag):
    for dag in dagbag.dags.values():
        check_cycle(dag)