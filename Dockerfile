FROM apache/airflow:3.3.1-python3.11


USER root
WORKDIR /app
RUN chown -R airflow: /app

# Install System Dependencies and Google Cloud SDK (gcloud CLI)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    unzip \
    procps \
    ca-certificates \
    gnupg \
    git \
    && mkdir -p /etc/apt/keyrings \
    && echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg \
    && apt-get update && apt-get install -y --no-install-recommends google-cloud-cli \
    && rm -rf /var/lib/apt/lists/*

# Install Starship Shell Prompt and configure for root and airflow users
RUN curl -sS https://starship.rs/install.sh | sh -s -- --yes \
    && echo 'eval "$(starship init bash)"' >> /root/.bashrc \
    && echo 'eval "$(starship init bash)"' >> /home/airflow/.bashrc

# Install Antigravity CLI (agy)
RUN curl -fsSL https://antigravity.google/cli/install.sh | bash -s -- --dir /usr/local/bin

USER airflow

ARG AIRFLOW_VERSION=3.3.1
ARG PYTHON_VERSION=3.11
ARG CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

COPY --chown=airflow:root requirements.txt .
COPY --chown=airflow:root tests/requirements-test.txt .

RUN pip install --no-cache-dir -r requirements.txt --constraint "${CONSTRAINT_URL}" \
    && pip install --no-cache-dir -r requirements-test.txt --constraint "${CONSTRAINT_URL}"

COPY --chown=airflow:root . .

# ENTRYPOINT []

CMD ["pytest", "-vvv","-p no:cacheprovider", "tests/"]