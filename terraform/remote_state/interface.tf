variable "prefix" {
  default     = "offwhite-dunk-tracker"
  description = "app name to prefix buckets with"
}

output "s3_bucket_id" {
  value = "aws_s3_bucket.remote_state.id"
}
