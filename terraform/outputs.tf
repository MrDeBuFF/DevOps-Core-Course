output "public_ip" {
  description = "Public IPv4 address of the VM"
  value       = yandex_compute_instance.vm.network_interface[0].nat_ip_address
}
