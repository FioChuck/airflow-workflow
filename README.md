# Airflow + Cloud Composer Workflow

This repository demonstrates an end-to-end Airflow workflow, from local development to automated deployment using Cloud Composer and Cloud Workstations on Google Cloud. It highlights best practices for dependency management, unit testing, and CI/CD integration.

## Summary

This repo covers the following:

- **Cloud Workstations:** Introduction to [Cloud Workstations](https://cloud.google.com/workstations/?e=48754805&hl=en) as an ephemeral development environment for [Airflow](https://airflow.apache.org/).
- **Local Development:** Developing Airflow DAGs locally with the [composer-dev](https://github.com/GoogleCloudPlatform/composer-local-dev) CLI tool. The steps outlined in this repo are similar/extension of the official docs found [here](https://cloud.google.com/composer/docs/composer-2/run-local-airflow-environments).
- **Unit Testing:** Implementing [unit tests](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#unit-tests) for Airflow DAGs using [Pytest](https://docs.pytest.org/en/stable/).
- **CI/CD:** Automating the deployment process with [Git Actions](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions) and [gcloud](https://cloud.google.com/sdk/gcloud).
- **Code Assist:** Leveraging [Gemini Code Assit](https://cloud.google.com/products/gemini/code-assist?e=48754805&hl=en) within the development environment.

## Development Challenges

Developing and deploying Airflow workflows presents several challenges:

- **Dependency Management:** Airflow, Python, PyPI packages, and Cloud Composer images have intricate dependencies that can be difficult to manage. For example, Airflow 2.3.0 dropped support for [Python 3.6](https://github.com/apache/airflow/pull/20467).
- **Environment Parity:** Ensuring consistency between local development and Cloud Composer environments.
- **Testing:** Effectively testing DAGs for functionality and potential issues.
- **CI/CD Integration:** Automating testing and deployment to streamline the workflow.

This demo addresses these challenges by leveraging Cloud Workstations, the `composer-dev` CLI tool, Pytest, and Git Actions.

## Detailed Breakdown

**1. Cloud Workstations**

- Ephemeral development environment with pre-configured tools and libraries.
- Securely connect to GCP resources within a VPC.
- Auto-shutdown capabilities to minimize costs.
- Integration with code assistance features like Gemini.

**2. Local Development with `composer-dev`**

- Create Composer containers locally that mirror Cloud Composer environments.
- Execute and test DAGs locally before deployment.
- Manage dependencies effectively.

**3. Unit Testing with Pytest**

- Write unit tests to validate DAG functionality.
- Test DAG imports and detect potential cycles.
- Ensure code quality and prevent errors.

**4. CI/CD with Git Actions**

- Automate the build, test, and deployment process.
- Enforce code quality through automated checks.
- Streamline the deployment workflow.

**5. Code Assist**

- Utilize code assistance features for improved productivity.
- Accelerate development with intelligent suggestions and auto-completion.

## Setup Steps

1.  **Set up Cloud Workstations:**

    - Create a Cloud Workstation instance within your VPC. This makes debugging connections to other GCP services like databases simple.
    - Connect to the workstation using [SSH](https://cloud.google.com/workstations/docs/develop-code-using-local-vscode-editor) or the web-based IDE.

2.  **Install Required Tools:**

    - Install [pyenv](https://github.com/pyenv/pyenv-virtualenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) using [Homebrew](https://docs.brew.sh/Homebrew-on-Linux). These tools will be used to run isolated Python environments.
    - Create two Python virtual environments:

      1. Python 3.11.10 for installing `composer-dev`. The [documentation](https://cloud.google.com/composer/docs/concepts/versioning/composer-versions#images-composer-2) states Python 3.8 through 3.11 is required.
      2. Python 3.11.9 for Airflow development and unit testing. I this example I used the _[composer-2.9.6-airflow-2.9.3]_ composer image with Python 3.11.9 released on 10/8/2024. Complete list of images found [here](https://cloud.google.com/composer/docs/concepts/versioning/composer-versions#images-composer-2).

    - List existing virtual environments:

    ```bash
    pyenv virtualenvs
    ```

    - Create a new virtual environments for CLI install and unit testing. Python version must already be installed using pyenv:

    ```bash
    pyenv virtualenv 3.11.10 install_env
    pyenv virtualenv 3.11.9 test_env
    ```

    - Activate install virtual environment to setup `composer-dev` cli tool:

    ```bash
    pyenv activate install_env
    ```

3.  **Install `composer-dev`:**

    - Clone the `composer-dev` repository:

    ```bash
    git clone https://github.com/GoogleCloudPlatform/composer-local-dev.git`
    ```

    - Navigate to the `projects/composer-dev` directory.
    - Install the CLI tool using pip:

    ```bash
    pip install .
    ```

4.  **Create a Local Composer Environment:**

    - Navigate to the `projects/airflow-workflow` directory.
    - Instrument the workaround for the issue found [here](https://github.com/GoogleCloudPlatform/composer-local-dev/issues/61).
    - List available images:

    ```bash
    composer-dev list-available-versions --include-past-releases --limit 10

    ```

    - Download image and setup file structure:

    ```bash
    composer-dev create \
    --from-image-version composer-2.9.6-airflow-2.9.3 \
    --dags-path ./dags \
    local-cc-dev
    ```

5.  **Start the Container:**

    - Start the local Composer container:

    ```bash
    composer-dev start local-cc-dev
    ```

    - Verify the Docker container is [running](https://docs.docker.com/reference/cli/docker/container/ls/):

    ```bash
    docker ps
    ```

6.  **Access the Airflow UI:**

    - Open a web browser and go to [http://localhost:8080](http://localhost:8080) to access the Airflow UI.

7.  **Explore the DAGs:**

    - Review the provided DAG examples:
      - **bq_details:**: Retrieves the dataset market_data and then lists all tables within that dataset, printing their names to the console.
      - **figlet:** Uses the pyfiglet library to print text in slant font to the console.
      - **bq_ctas:** Executes a BigQuery query to create or replace a table named googl*daily_bar with aggregated daily market data for Google *(GOOGL)\_ including symbol, date, and closing price.

8.  **Unit Testing:**

    - Activate the `test_env` Python virtual environment:

    ```bash
    pyenv activate test_env
    ```

    - Install libsqlite3-dev. This is a known build problem with Pyenv outlined [here](https://github.com/pyenv/pyenv/wiki/Common-build-problems). The problem is documented in issue #678 found [here](https://github.com/pyenv/pyenv/issues/678).

    ```bash
    sudo apt install libsqlite3-dev
    ```

    - Install the requirements and test requirements files using [-r flags](https://pip.pypa.io/en/stable/user_guide/#requirements-files):

    ```bash
    pip install -r composer/local-cc-dev/requirements.txt
    pip install -r tests/requirements-test.txt
    ```

    - Run the tests cases with [verbose flag enabled](https://docs.pytest.org/en/stable/reference/reference.html#command-line-flags):

    ```bash
    pytest -v
    ```

9.  **CI/CD with Git Actions:**

    - The Git Actions in the workflow found in `/.github/workflows/deployer.yaml` rely on the following action secrets:

      - **IDENTITY_PROVIDER:** Workload identity provider used for [identity federation](https://cloud.google.com/iam/docs/workload-identity-federation). Identify federation is instrumented using the [google-github-actions/auth](https://github.com/google-github-actions/auth) action. The action documentation has instructions for setting up an identity pool and provider.

        This value typically takes the form `projects/{project number}/locations/global/workloadIdentityPools/{workload-identity-pool}/providers/{workload-identity-provider}`.

        You can print the value required for this secret using gcloud iam [gcloud iam workload-identity-pools describe](https://cloud.google.com/sdk/gcloud/reference/iam/workload-identity-pools/describe).

        More information on keyless authentication with Git Actions [here](https://cloud.google.com/blog/products/identity-security/enabling-keyless-authentication-from-github-actions?e=48754805).

      - **SA:** Service account impersonated by identity provider.

    - Refer to the CI/CD best practices in the Google Cloud documentation found [here](https://cloud.google.com/composer/docs/dag-cicd-integration-guide).
