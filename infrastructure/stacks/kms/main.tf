
resource "aws_kms_key" "ear_key_test" {
  description         = "KMS Keys for Data Encryption"
  customer_master_key_spec = "SYMMETRIC_DEFAULT"
  is_enabled               = true
  enable_key_rotation      = true 

  tags = {
    service = var.project_id
  }
}

resource "aws_kms_alias" "my_kms_alias" {
  target_key_id = aws_kms_key.my_kms_key.key_id
  name          = "alias/${var.kms_alias}"
}

output "key_id" {
  value = aws_kms_key.my_kms_key.key_id
}