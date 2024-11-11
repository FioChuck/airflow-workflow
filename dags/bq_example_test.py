from airflow import models
from airflow.utils.dag_cycle_tester import test_cycle
import pytest
from airflow.models import DagBag


@pytest.fixture
def test_dagbag():
    dag_bag = DagBag(include_example=False)
    assert not dag_bag.import_errors
