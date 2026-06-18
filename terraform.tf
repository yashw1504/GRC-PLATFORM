resource "aws_s3_bucket" "demo" {

  bucket = "demo"

  acl = "public-read"
}

resource "aws_security_group" "demo" {

  ingress {

    from_port = 22

    to_port = 22

    protocol = "tcp"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }
}