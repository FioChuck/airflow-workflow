FROM apache/airflow:2.9.3-python3.9


COPY entrypoint.sh /entrypoint.sh

USER root
WORKDIR /app
RUN chown -R airflow: /app

USER airflow


COPY --chown=airflow:root composer/local-cc-dev/requirements.txt .
COPY --chown=airflow:root tests/requirements-test.txt .


RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-test.txt

COPY --chown=airflow:root . .

ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

ENTRYPOINT ["/entrypoint.sh"]

CMD ["pytest", "-vvv","-p no:cacheprovider", "tests/"]