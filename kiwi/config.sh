#!/bin/bash

set -euxo pipefail

test -f /.kconfig && . /.kconfig
test -f /.profile && . /.profile

echo "Configure image..."

#======================================
# Clear machine specific configuration
#--------------------------------------
## Clear machine-id on pre generated images
rm -f /etc/machine-id
touch /etc/machine-id
## remove random seed, the newly installed instance should make its own
rm -f /var/lib/systemd/random-seed

#======================================
# Delete & lock the root user password
#--------------------------------------
passwd -d root
passwd -l root

#======================================
# Setup default services
#--------------------------------------
systemctl enable NetworkManager.service
systemctl enable chronyd.service
systemctl enable sddm.service
systemctl enable zramswap.service

mkdir -p /var/log/journal

systemctl set-default graphical.target

#======================================
# Enable yast2-firstboot
#--------------------------------------
touch /var/lib/YaST2/reconfig_system

#======================================
# Generate boot.bin
#--------------------------------------
mkdir -p /boot/efi/m1n1
update-m1n1 /boot/efi/m1n1/boot.bin
rm -rf /boot/.builder

#======================================
# Update GRUB2
#--------------------------------------
grub2-mkconfig -o /boot/grub2/grub.cfg

#======================================
# Default to Wayland
#--------------------------------------
cat > /usr/lib/sddm/sddm.conf.d/10-wayland-default.conf <<EOF
[General]
DisplayServer=wayland
EOF

exit 0
