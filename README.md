# Pull Request Analysis Tool

A pull requests and comment analytics tool.

## Pre-Requisites
1. Generate a GitHub API Token.

2. Copy `example_config.json` to `config.json` and update values like GitHub API token, repository owners (for example `bovem`) and repository names (for example `pr-analysis-tool`)

## Deployment
1. Create necessary sub-directories in project's root directory.
```bash
mkdir -p ./app/raw_data/
mkdir -p ./app/cleaned_data/
mkdir -p ./app/metrics_data/
mkdir -p ./postgres-data/
```

2. Deploy containers
```bash
docker compose up -d
```

3. Visit Grafana dashbaord at [localhost:3111](http://localhost:3111)

4. Configure PostgreSQL [Data Connection](http://localhost:3111/connections/datasources) with the values provided in [docker-compose](./compose.yaml) file.

5. Open **Pull Request and PipelineRun Statistics Dashboard**.

## Updating Data
```bash
docker exec -it pr-analysis-tool-backend-1 python3 parallel_main.py
```
