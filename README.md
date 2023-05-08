# stock-market-analysis

This project is part of the "Proyecto Aplicado en Analítica de Datos" course at the University of Los Andes.

## 1. Context

The Stanley Group is one of the most relevant financial conglomerates in Latin America. It presents two main strategic visions, the first is the management of innovation in financial products, and the second is the Money Desk, which is more related to capital market products and has a greater impact on the financial performance of the group, as its current loss situation is around $7 million USD, while for the former, its losses are close to $250 thousand USD.

Among the main financial services managed by the Money Desk are equity investments, asset management, portfolio management, mergers and acquisitions. Regarding performance measures associated with the project, the financial performance of the group (gross margin and profitability), customer satisfaction (positive ratings vs. total ratings), and the turnover rate of human talent should be taken into account, which is related to additional costs due to its management and maintenance.

## 2. Data

The data for this project will be obtained by making daily calls to the Polygon API. The API documentation can be found at: [https://polygon.io/docs/stocks/getting-started](https://polygon.io/docs/stocks/getting-started).

For this project, we will be taking data from the top 15 companies that are part of the S&P500 index. This will include the following stock symbols:

- AAPL (Apple Inc.)
- MSFT (Microsoft Corporation)
- AMZN (Amazon.com, Inc.)
- META (Meta Platforms, Inc.)
- GOOGL (Alphabet Inc. Class A)
- GOOG (Alphabet Inc. Class C)
- TSLA (Tesla, Inc.)
- JPM (JPMorgan Chase & Co.)
- JNJ (Johnson & Johnson)
- BRK.B (Berkshire Hathaway Inc. Class B)
- V (Visa Inc.)
- PG (Procter & Gamble Company)
- NVDA (NVIDIA Corporation)
- UNH (UnitedHealth Group Incorporated)
- XOM (Exxon)

This data will be used to analyze the performance of these companies in the stock market and to predict possible future trends.

## 3. Architecture

The architecture for this project involves defining AWS resources through Infrastructure As Code using Terraform. AWS EC2 servers are deployed to make calls to the Polygon API through Airbyte. The data is then stored in an AWS S3 data lake before being passed to a data warehouse in Snowflake where it is transformed into RAW, PREPARED, and CURATED schemas for serving to end-users on a PowerBI dashboard.

![Architecture](images/architecure.png)

This architecture was chosen for its ability to handle large amounts of data and for its scalability. Defining resources through Infrastructure As Code with Terraform allows for efficient management and deployment of resources in a reproducible and scalable way. AWS EC2 servers provide a reliable and cost-effective way to make API calls, while Airbyte allows for seamless data integration from multiple sources. Storing the data in an AWS S3 data lake allows for easy access and retrieval of the data, while Snowflake provides a powerful data warehousing solution with support for multiple data types and seamless integration with other AWS services. Finally, the data is transformed for optimized performance and efficient querying. The PowerBI dashboard provides a user-friendly interface for end-users to interact with the data and gain insights.

## 4. Set up

### 4.1 AWS Infrastructure

The AWS infrastructure is managed through IaC (Infrastructure as Code) using Terraform. The environment is defined in configuration files within the [infrastructure](https://github.com/ricardo8aib/stock-market-analysis/tree/main/infrastructure) folder, which we can version, control, and replicate more effectively than if we used manual processes to configure our servers.
This includes the EC2 server with Airbyte and the S3 bucket that will serve as a data lake. Also all the parameters needed such as names and credentiasl can be replicated based on the [.env.template file](https://github.com/ricardo8aib/stock-market-analysis/blob/main/.env.template).

#### 4.1.1 Airbyte EC2 Instance

The terraform files genereate an EC2 instance with Airbyte running on the `8000 port`.  

The instance installs `docker` and `docker-compose` during the start-up. Other tools
can be installed during the start-up by modifying the `user_data` param from the `ec2_instance` resource in the `main.tf` file.

The `terraform.tfvars` contains basic configurations for the instance and the AWS profile. The `profile` variable indicates terraform which AWS profile should be used to deploy the infrastructure. By default, terraform checks the AWS profiles in `~/.aws/credentials`.
The `AMI`, `instance type` and `instance size` can be also set there. This project uses a `t2.small` machine with a `ami-052efd3df9dad4825` AMI.

This instance can be initialized using the make command `make create-ec2-airbyte` from the root directory of this repo.

Once the Airbyte instance is `Running`, it's possible to access the Airflow Web App through the instance `Public IPv4 address` and the `port 8000`.  
The user is `airbyte` and the password is `password`.

#### 4.1.2 Stage S3 bucket

The terraform files generate an S3 bucket, and the IAM role and policy required to let Snowflake access the bucket. The resources created in this Terraform module only apply to AWS. To have a functional stage other steps must be followed later with Snowflake.

This bucket can be initialized using the make command `make create-s3-snowflake-stage` from the root directory.

### 4.2 Snowflake

The whole Snowflake set up can be done using the `make` commands. The code that executes each of the steps is hosted in the [src folder](https://github.com/ricardo8aib/stock-market-analysis/tree/main/src) and a `.env` file is used to get the parameters. Again, all the parameters needed such as names and credentiasl can be replicated based on the [.env.template file](https://github.com/ricardo8aib/stock-market-analysis/blob/main/.env.template).

#### 4.2.1 Database

The make command `make setup-snowflake` from the root directory of this repo creates the database and the schemas needed for the data pipeline.

#### 4.2.2 Ingestion

The make command `make ingestion` from the root directory of this repo creates the stage, storage integration and tables that will be used.

#### 4.2.3 Tasks

The make command `make tasks` from the root directory of this repo creates the tasks that will ingest and clean the data from the data lake.

#### 4.2.4 Views

The make command `make views` from the root directory of this repo creates the views from the prepared tables.

#### 4.2.5 Permissions

The make command `make permissions` from the root directory of this repo grants the permissions to use the database, schema and views to an assigned user.

## Analysis

Description of the analysis performed on the data.

## Results

Summary of the results obtained from the analysis.

## Conclusion

Conclusions drawn from the results and any further recommendations.

## Authors

- **Ricardo Ibarra** [ricardo8aib](https://github.com/ricardo8aib)
- **Cristian Hernandez** [crisheal17](https://github.com/Crisheal17)
- **Juan Sebastián Delgado** [jsdelgadoc0117](https://github.com/jsdelgadoc0117)
- **David Zuluaga** [davidzuluagagomez](https://github.com/davidzuluagagomez)
