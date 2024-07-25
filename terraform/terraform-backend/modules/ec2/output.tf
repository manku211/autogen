# output "public_key" {
#   value = file("~/.ssh/id_rsa.pub")
# }

output "private_key_path" {
  value = local_file.ssh_key[0].filename
}

output "instance_id" {
  value = aws_instance.e1[0].id
}

output "public_ip" {
  value = aws_instance.e1[0].public_ip
}