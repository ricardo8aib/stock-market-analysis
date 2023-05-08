# A Self-Documenting Makefile: http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
SHELL = /bin/bash
OS = $(shell uname | tr A-Z a-z)

.PHONY: format
format: ## Formats code
	poetry run black .
	poetry run isort .

# EC2 Airbyte infrastructure
.PHONY: create-ec2-airbyte
create-ec2-airbyte: ## Create infrastructure - airbyte EC2
	(cd infrastructure/ec2-airbyte; terraform init; terraform apply -auto-approve)
	chmod 600 infrastructure/ec2-airbyte/keys/*.pem

.PHONY: destroy-ec2-airbyte
destroy-ec2-airbyte: ## Destroy infrastructure - airbyte EC2
	(cd infrastructure/ec2-airbyte; terraform destroy -auto-approve)
	rm -rf infrastructure/ec2-airbyte/keys/*.pem

# S3 stage infrastructure
.PHONY: create-s3-snowflake-stage
create-s3-snowflake-stage: ## Create infrastructure - S3 Snowflake stage bucket
	(cd infrastructure/s3-snowflake-stage; terraform init; terraform apply -auto-approve)

.PHONY: destroy-s3-snowflake-stage
destroy-s3-snowflake-stage: ## Destroy infrastructure - S3 Snowflake stage bucket
	(cd infrastructure/s3-snowflake-stage; terraform destroy -auto-approve)
	rm -rf infrastructure/s3-snowflake-stage/*.zip



# Snowflake setup and data ingestion
.PHONY: clean-snowflake
clean-snowflake: ## Drop Snowflake database and storage integration
	poetry run python src/clean-up/clean.py

.PHONY: setup-snowflake
setup-snowflake: ## Create the database and schema for the project
	poetry run python src/database/database.py

.PHONY: ingestion
ingestion: ## Run ingestion script
	poetry run python src/ingestion/ingestion.py

.PHONY: tasks
tasks: ## Run tasks script
	poetry run python src/tasks/tasks.py

.PHONY: views
views: ## Run views script
	poetry run python src/views/views.py

.PHONY: permissions
permissions: ## Run permissions script
	poetry run python src/permissions/permissions.py

.PHONY: manual
permissions: ## Run manual script
	poetry run python src/permissions/manual.py
