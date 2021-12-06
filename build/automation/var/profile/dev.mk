-include $(VAR_DIR)/platform-texas/v1/account-live-k8s-nonprod.mk

# ==============================================================================
# Service variables

LOG_LEVEL := INFO
DOS_API_GATEWAY_SECRETS := $(TF_VAR_dos_api_gateway_secret)
DOS_API_GATEWAY_USERNAME_KEY := DOS_API_GATEWAY_USERNAME
DOS_API_GATEWAY_PASSWORD_KEY := DOS_API_GATEWAY_PASSWORD
DOS_API_GATEWAY_USERNAME := $(or $(DOS_API_GATEWAY_USERNAME), "")
DOS_API_GATEWAY_PASSWORD := $(or $(DOS_API_GATEWAY_PASSWORD), "")
DOS_API_GATEWAY_REQUEST_TIMEOUT := 30
DOS_API_GATEWAY_URL := $(or $(DOS_API_GATEWAY_MOCK_URL), "//")
MOCK_MODE := False


DB_SERVER := uec-core-dos-regression-db-9-replica-pu
DB_PORT := 5432
DB_NAME := pathwaysdos_regression
DB_SCHEMA := pathwaysdos
DB_SECRET_NAME := core-dos-dev/deployment
DB_SECRET_KEY := DB_SF_READONLY_PASSWORD
DB_USER_NAME_SECRET_NAME = uec-dos-int-dev/deployment
DB_USER_NAME_SECRET_KEY = DOS_REPLICA_DI_USERNAME
TF_VAR_dos_db_name := uec-core-dos-regression-db-9-replica-pu
# ==============================================================================
# Infrastructure variables (Terraform, Serverless, etc)

# API Gateway API Keys
TF_VAR_api_gateway_api_key_name := $(PROJECT_ID)-$(PROFILE)-api-key
TF_VAR_nhs_uk_api_key_key := NHS_UK_API_KEY

# Lambda Security Group
TF_VAR_lambda_security_group_name := $(PROJECT_ID)-$(ENVIRONMENT)-lambda-sg

# API Gateway Route53
TF_VAR_dos_integration_sub_domain_name := $(PROGRAMME)-$(TEAM_ID)-$(ENVIRONMENT)
DOS_INTEGRATION_URL := $(TF_VAR_dos_integration_sub_domain_name).$(TEXAS_HOSTED_ZONE)

# DoS API Gateway Mock
TF_VAR_dos_api_gateway_name := $(PROJECT_ID)-$(ENVIRONMENT)-dos-api-gateway-mock
TF_VAR_dos_api_gateway_stage := $(ENVIRONMENT)
TF_VAR_dos_api_gateway_authoriser := $(PROJECT_ID)-$(ENVIRONMENT)-dos-api-gateway-mock-authoriser
TF_VAR_authoriser_lambda_name := $(PROJECT_ID)-$(ENVIRONMENT)-authoriser
TF_VAR_image_version := $(or $(VERSION), latest)
TF_VAR_dos_api_gateway_secret := $(PROJECT_ID)-$(ENVIRONMENT)-dos-api-gateway-mock-secret
DOS_API_GATEWAY_MOCK_URL := https://$(TF_VAR_dos_api_gateway_name).$(TEXAS_HOSTED_ZONE)/change-request
TF_VAR_dos_api_gateway_secret_username_key := $(DOS_API_GATEWAY_USERNAME_KEY)
TF_VAR_dos_api_gateway_secret_password_key := $(DOS_API_GATEWAY_PASSWORD_KEY)
TF_VAR_dos_api_gateway_lambda_name := $(PROJECT_ID)-$(ENVIRONMENT)-dos-api-gateway-lambda
