##########################
# INFRASTRUCTURE COMPONENT
##########################

############
# AWS COMMON
############

variable "aws_profile" {
  description = "The AWS profile"
}

variable "aws_region" {
  description = "The AWS region"
}

variable "aws_account_id" {
  description = "AWS account Number for Athena log location"
}

# ##############
# # TEXAS COMMON
# ##############

variable "profile" {
  description = "The tag used to identify profile e.g. dev, test, live, ..."
}

variable "texas_s3_logs_bucket" {
  description = "The texas s3 log bucket for s3 bucket logs"
}

variable "terraform_platform_state_store" {
  description = "platform state store"
}

variable "vpc_terraform_state_key" {
  description = "vpc state key"
}

variable "programme" {
  description = "Programme name"
}

variable "project_id" {
  description = "Project ID"
}

variable "environment" {
  description = "Environment name"
}

# ############################
# # Common
# ############################

variable "route53_terraform_state_key" {
  description = "terraform state key"
}

variable "team_id" {
  description = "team id"
}

# ############################
# API GATEWAY
# ############################

variable "di_endpoint_api_gateway_name" {
  description = ""
}

variable "di_endpoint_api_gateway_stage" {
  description = ""
}


# ############################
# SQS
# ############################

variable "fifo_queue_name" {
  description = ""
}

variable "event_processor_lambda_name" {
  description = ""
}

# ############################
# # ROUTE53
# ############################

variable "dos_integration_sub_domain_name" {
  type        = string
  description = "sub domain name"
}

variable "texas_hosted_zone" {
  description = "hosted zone"
}

# ############################
# # SECRETS
# ############################

variable "api_gateway_api_key_name" {
  description = "API Key for DI AWS API Gateway"
}

variable "nhs_uk_api_key_key" {
  description = "API Key key for secrets manager"
}