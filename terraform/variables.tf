variable "zone" {
  description = "Availability zone for resources"
  type        = string
  default     = "ru-central1-a"
}

variable "folder_id" {
  description = "Yandex Cloud folder ID"
  type        = string
}

variable "ssh_user" {
  description = "Linux user for SSH access"
  type        = string
  default     = "ubuntu"
}

variable "ssh_public_key" {
  description = "Path to SSH public key"
  type        = string
}

