# AWS EC2 Instances

resource "aws_instance" "my_ec2_instance" {

  ami           = "ami-12345abcde"

  instance_type = "t2.micro"

  subnet_id = "subnet-6789fghij"

  tags = {

    "Name" = "MyEC2Instance"

    "Project" = "MyProject"

  }

}
