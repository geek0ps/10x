# S3 Buckets

resource "aws_s3_bucket" "my-unique-bucket-name" {

  bucket = "my-unique-bucket-name"

  acl    = "private"

  tags = {

    "Environment" = "Development"

  }

}
