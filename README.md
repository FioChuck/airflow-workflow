# Airflow Workflow with Cloud Composer

This repository demonstrates an end-to-end Airflow workflow, from local development to automated deployment using Cloud Composer and Cloud Workstations. It highlights best practices for dependency management, unit testing, and CI/CD integration.

## Summary

This outline covers the following:

- **Cloud Workstations:** Introduction to [Cloud Workstations](https://cloud.google.com/workstations/?e=48754805&hl=en) as an ephemeral development environment for [Airflow](https://airflow.apache.org/).
- **Local Development:** Developing Airflow DAGs locally with the [composer-dev](https://github.com/GoogleCloudPlatform/composer-local-dev) CLI tool.
- **Unit Testing:** Implementing unit tests for Airflow DAGs using [Pytest](https://docs.pytest.org/en/stable/).
- **CI/CD:** Automating the deployment process with [Git Actions](https://docs.github.com/en/actions/about-github-actions/understanding-github-actions) and [gcloud](https://cloud.google.com/sdk/gcloud).
- **Code Assist:** Leveraging [Gemini Code Assit](https://cloud.google.com/products/gemini/code-assist?e=48754805&hl=en) within the development environment.

## Development Challenges

Developing and deploying Airflow workflows presents several challenges:

- **Dependency Management:** Airflow, Python, PyPI packages, and Cloud Composer images have intricate dependencies that can be difficult to manage.
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

    - Create a Cloud Workstation instance within your VPC. This makes debugging connections to other GCP services like databaes simple.
    - Connect to the workstation using [SSH](https://cloud.google.com/workstations/docs/develop-code-using-local-vscode-editor) or the web-based IDE.

2.  **Install Required Tools:**

    - Install [pyenv](https://github.com/pyenv/pyenv-virtualenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) using [Homebrew](https://docs.brew.sh/Homebrew-on-Linux).
    - Create two Python virtual environments:
      1. Python 3.11.10 for installing `composer-dev`.
      2. Python 3.10.9 for Airflow development and unit testing.
    - List existing virtual environments:

    ```bash
    pyenv virtualenvs
    ```

    - List existing virtual environments:

    ```bash
    pyenv virtualenv 3.11.10 install_env
    ```

    - Activate virtual environment:

    ```bash
    pyenv activate install_env
    ```

3.  **Install `composer-dev`:**

    - Clone the `composer-dev` repository:

    ```bash
    git clone https://github.com/GoogleCloudPlatform/composer-local-dev.git`
    ```

    - Navigate to the `projects/composer-dev` directory.
    - Install the CLI tool:

    ```bash
    pip install .
    ```

4.  **Create a Local Composer Environment:**

    - Navigate to the `projects/airflow-workflow` directory.
    - Instrument Docer error workaround found [here](https://github.com/GoogleCloudPlatform/composer-local-dev/issues/61)
    - Run:

    ```bash
    composer-dev create \
    --from-image-version composer-2.9.6-airflow-2.9.3 \
    --dags-path ./dags \
    local-cc-dev
    ```

5.  **Start the Container:**

    - Run `composer-dev start local-cc-dev` to start the container.

6.  **Access the Airflow UI:**

    - Open a web browser and go to `http://localhost:8080` to access the Airflow UI.

7.  **Explore the DAGs:**

    - Review the provided DAG examples (`bq_details`, `figlet`, `bq_ctas`).

8.  **Unit Testing:**

    - Activate the `pytest_env` virtual environment.
    - Install the test requirements: `pip install -r tests/requirements-test.txt`.
    - Run the tests: `pytest -s`.

9.  **CI/CD with Git Actions:**

    - Configure a Git Actions workflow to automate testing and deployment.
    - Refer to the CI/CD best practices in the Google Cloud documentation.

## Open Items

- Known issues when installing Airflow with `pyenv`.
- Keyless authentication from GitHub Actions.

## Resources

- [Cloud Composer Documentation](https://cloud.google.com/composer)
- [Cloud Workstations Documentation](https://www.google.com/url?sa=E&source=gmail&q=https://cloud.google.com/workstations)
- [Airflow Documentation](https://www.google.com/url?sa=E&source=gmail&q=https://airflow.apache.org/)
- [Pytest Documentation](https://www.google.com/url?sa=E&source=gmail&q=https://docs.pytest.org/)
- [Git Actions Documentation](https://www.google.com/url?sa=E&source=gmail&q=https://docs.github.com/en/actions)
