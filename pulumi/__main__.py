import pulumi
import pulumi_yandex as yc
from pathlib import Path

config = pulumi.Config()

network = yc.VpcNetwork(
    "lab4-network"
)

subnet = yc.VpcSubnet(
    "lab4-subnet",
    network_id=network.id,
    zone="ru-central1-a",
    v4_cidr_blocks=["10.0.0.0/24"],
)

sg = yc.VpcSecurityGroup(
    "lab4-sg",
    network_id=network.id,
)


# SSH
yc.VpcSecurityGroupRule(
    "ssh-ingress",
    security_group_binding=sg.id,
    direction="ingress",
    protocol="TCP",
    port=22,
    v4_cidr_blocks=["0.0.0.0/0"],
)

# HTTP
yc.VpcSecurityGroupRule(
    "http-ingress",
    security_group_binding=sg.id,
    direction="ingress",
    protocol="TCP",
    port=80,
    v4_cidr_blocks=["0.0.0.0/0"],
)

# Flask / App
yc.VpcSecurityGroupRule(
    "flask-ingress",
    security_group_binding=sg.id,
    direction="ingress",
    protocol="TCP",
    port=5000,
    v4_cidr_blocks=["0.0.0.0/0"],
)

# Egress (всё наружу)
yc.VpcSecurityGroupRule(
    "all-egress",
    security_group_binding=sg.id,
    direction="egress",
    protocol="ANY",
    v4_cidr_blocks=["0.0.0.0/0"],
)

image = yc.get_compute_image(
    family="ubuntu-2204-lts"
)

ssh_key_path = Path.home() / ".ssh" / "id_ed25519.pub"
ssh_key = ssh_key_path.read_text().strip()

vm = yc.ComputeInstance(
    "lab4-vm",
    zone="ru-central1-a",
    platform_id="standard-v2",
    resources=yc.ComputeInstanceResourcesArgs(
        cores=2,
        memory=1,
        core_fraction=20,
    ),
    boot_disk=yc.ComputeInstanceBootDiskArgs(
        initialize_params=yc.ComputeInstanceBootDiskInitializeParamsArgs(
            image_id=image.id,
            size=10,
        )
    ),
    network_interfaces=[
        yc.ComputeInstanceNetworkInterfaceArgs(
            subnet_id=subnet.id,
            nat=True,
            security_group_ids=[sg.id],
        )
    ],
    metadata={
        "ssh-keys": f"ubuntu:{ssh_key}",
    },
)

pulumi.export(
    "public_ip",
    vm.network_interfaces[0].nat_ip_address
)
