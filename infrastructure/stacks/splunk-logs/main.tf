resource "aws_cloudwatch_log_subscription_filter" "event_receiver_logs_subscription_filter" {
  name            = var.event_receiver_subscription_filter_name
  role_arn        = data.aws_iam_role.firehose_role.arn
  log_group_name  = "/aws/lambda/${var.event_receiver_lambda_name}"
  filter_pattern  = ""
  destination_arn = data.aws_kinesis_firehose_delivery_stream.dos_integration_firehose.arn
  distribution    = ""
}

resource "aws_cloudwatch_log_subscription_filter" "event_processor_logs_subscription_filter" {
  name            = var.event_processor_subscription_filter_name
  role_arn        = data.aws_iam_role.firehose_role.arn
  log_group_name  = "/aws/lambda/${var.event_processor_lambda_name}"
  filter_pattern  = ""
  destination_arn = data.aws_kinesis_firehose_delivery_stream.dos_integration_firehose.arn
  distribution    = ""
}

resource "aws_cloudwatch_log_subscription_filter" "event_sender_logs_subscription_filter" {
  name            = var.event_sender_subscription_filter_name
  role_arn        = data.aws_iam_role.firehose_role.arn
  log_group_name  = "/aws/lambda/${var.event_sender_lambda_name}"
  filter_pattern  = ""
  destination_arn = data.aws_kinesis_firehose_delivery_stream.dos_integration_firehose.arn
  distribution    = ""
}