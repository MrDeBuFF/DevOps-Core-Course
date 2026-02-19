variable "zone" {
  description = "YC zone"
  default     = "ru-central1-a"
}

variable "folder_id" {
  description = "YC folder id"
}

variable "ssh_user" {
  default = "ubuntu"
}

variable "ssh_public_key" {
  description = "Path to SSH public key"
}
