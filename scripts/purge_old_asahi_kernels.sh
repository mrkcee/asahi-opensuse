#!/usr/bin/sh

if [ "$(whoami)" != "root" ]; then
    echo "Script must be run as root" >&2
    exit 1
fi

current_kernel=`uname -r | sed 's/asahi-//'`

echo "This script uninstalls old kernel-asahi packages. Only the current kernel will be retained."
echo "Current kernel: $current_kernel"

installed_kernels=`rpm -qa | grep -i kernel-asahi | sort -r | sed 's/kernel-asahi-//' | sed 's/.aarch64//'`

packages_to_be_removed=""

for pkg in $installed_kernels
do
  if [ "$pkg" != "$current_kernel" ]; then
    packages_to_be_removed+=" kernel-asahi=$pkg"
  fi 
done

if [ -n "$packages_to_be_removed" ]; then
  zypper rm $packages_to_be_removed
  echo "Note: old initrd files in /boot need to be manually deleted."
else
  echo "Nothing to do."
fi

