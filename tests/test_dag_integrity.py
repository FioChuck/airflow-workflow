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


def test_all_dags_loaded(dagbag):

    assert dagbag.import_errors == {}, "Import errors"
    assert len(dagbag.dags) > 0, "DagBag is empty"

    for dag_id, dag in dagbag.dags.items():
        assert dag is not None, f"DAG '{dag_id}' failed to load"
        assert len(dag.tasks) > 0, f"DAG '{dag_id}' has no tasks"


def test_dag_cycles(dagbag):
    for dag in dagbag.dags.values():
        check_cycle(dag)
