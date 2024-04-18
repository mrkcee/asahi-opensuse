%define _rcver 6.6
%define _asahirel 16
%define _commit_id asahi-%{_rcver}-%{_asahirel}

Name: kernel-asahi
Summary: The Linux Kernel
Version: 6.6.27
Release: 2
License: GPL
Group: System Environment/Kernel
Vendor: The Linux Community
URL: https://www.kernel.org
Source0: https://github.com/AsahiLinux/linux/archive/refs/tags/%{_commit_id}.tar.gz
Source1: config-asahi-%{version}
# Compressed patch files from kernel-source repo
Source2: patch-%{version}.tar.gz
# Speaker enablement patches
Patch0: 10-speakers-enable-part1.patch
Patch1: 10-speakers-enable-part2.patch
BuildRequires: bc binutils bison dwarves
BuildRequires: (elfutils-libelf-devel or libelf-devel) flex
BuildRequires: gcc make openssl openssl-devel perl python3 rsync
# TODO: add BuildRequires for rustc bindgen when installed via rustup
#BuildRequires: rust rust-bindgen
Provides:       %name = %version-%release
Provides:       %name-%version-%release
Provides:       %{name}_%_target_cpu = %version-%release
Provides:       kernel-base = %version-%release
Provides:       kernel = %version-%release
Provides:       multiversion(kernel)
Conflicts:      filesystem < 16
Obsoletes:      microcode_ctl < 1.18
BuildRequires:  zstd
Requires(post): modutils
Requires(post): kmod-zstd
Requires(post): dracut
%description
The Linux Kernel, the operating system core itself

# how the kernel release string (uname -r) should look like
%define kernelrelease %{version}-asahi

# aarch64 as a fallback of _arch in case
# /usr/lib/rpm/platform/*/macros was not included.
%define _arch %{?_arch:aarch64}
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}

# TW is usrmerged
%if 0%{?suse_version} >= 1550
%define usrmerged 1
%else
%define usrmerged 0
%endif

%if %{usrmerged}
%define kernel_module_directory /usr/lib/modules
%else
%define kernel_module_directory /lib/modules
%endif

%prep
%setup -n linux-%{_commit_id} -q
%patch 0 -p1
%patch 1 -p1

tar xzf %{_sourcedir}/patch-6.6.27.tar.gz
# Remove patches that conflict with Asahi-specific changes or were applied already
# Some will have to be manually applied/merged
rm patches.kernel.org/6.6.1-015-Bluetooth-hci_bcm4377-Mark-bcm4378-bcm4387-as-B.patch 
rm patches.kernel.org/6.6.2-532-regmap-prevent-noinc-writes-from-clobbering-cac.patch
rm patches.kernel.org/6.6.2-475-xhci-Loosen-RPM-as-default-policy-to-cover-for-.patch
rm patches.kernel.org/6.6.3-287-regmap-Ensure-range-selector-registers-are-upda.patch
rm patches.kernel.org/6.6.3-411-xhci-Enable-RPM-on-controllers-that-support-low.patch
rm patches.kernel.org/6.6.5-050-iommu-Avoid-more-races-around-device-probe.patch
rm patches.kernel.org/6.6.5-126-iommu-Fix-printk-arg-in-of_iommu_get_resv_regio.patch
rm patches.kernel.org/6.6.7-208-ASoC-ops-add-correct-range-check-for-limiting-v.patch
rm patches.kernel.org/6.6.7-216-Revert-xhci-Loosen-RPM-as-default-policy-to-cov.patch
rm patches.kernel.org/6.6.14-350-rust-Ignore-preserve-most-functions.patch
rm patches.kernel.org/6.6.14-495-iommu-Don-t-reserve-0-length-IOVA-region.patch
rm patches.kernel.org/6.6.17-012-rust-arc-add-explicit-drop-around-Box-from_raw.patch
rm patches.kernel.org/6.6.17-013-rust-upgrade-to-Rust-1.72.1.patch
rm patches.kernel.org/6.6.17-016-rust-upgrade-to-Rust-1.73.0.patch
rm patches.kernel.org/6.6.19-004-dmaengine-apple-admac-Keep-upper-bits-of-REG_B.patch
rm patches.kernel.org/6.6.24-004-wifi-brcmfmac-Fix-use-after-free-bug-in-brcmf_.patch
rm patches.kernel.org/6.6.24-185-wifi-brcmfmac-add-per-vendor-feature-detection.patch
rm patches.kernel.org/6.6.24-186-wifi-brcmfmac-cfg80211-Use-WSEC-to-set-SAE-pas.patch
rm patches.kernel.org/6.6.24-187-wifi-brcmfmac-Demote-vendor-specific-attach-de.patch
rm patches.kernel.org/6.6.24-358-usb-dwc3-Properly-set-system-wakeup.patch

for f in `ls -v ./patches.kernel.org/*.patch`; do
	patch -p1 -F0 -i $f
done

# Apply RPM-related patches
tar xzf %{_sourcedir}/patches-rpmify.tar.gz
for f in ./patches.rpmify/*.patch; do
	patch -p1 -F0 -i $f
done

# Apply SUSE-specific patches
tar xzf %{_sourcedir}/patches-suse.tar.gz
patch -p1 -F0 -i patches.suse/lib-ucs2_string-Add-UCS-2-strscpy-function.patch
patch -p1 -F0 -i patches.suse/firmware-qemu_fw_cfg-Do-not-hard-depend-on-CONFIG_HA.patch
patch -p1 -F0 -i patches.suse/rpm-kernel-config
patch -p1 -F0 -i patches.suse/add-suse-supported-flag.patch
patch -p1 -F0 -i patches.suse/genksyms-add-override-flag.diff
patch -p1 -F0 -i patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
patch -p1 -F0 -i patches.suse/kernel-add-release-status-to-kernel-build.patch
patch -p1 -F0 -i patches.suse/panic-do-not-print-uninitialized-taint_flags.patch
patch -p1 -F0 -i patches.suse/readahead-request-tunables.patch
patch -p1 -F0 -i patches.suse/vfs-add-super_operations-get_inode_dev
patch -p1 -F0 -i patches.suse/btrfs-provide-super_operations-get_inode_dev
patch -p1 -F0 -i patches.suse/btrfs-8447-serialize-subvolume-mounts-with-potentially-mi.patch
patch -p1 -F0 -i patches.suse/b43-missing-firmware-info.patch
patch -p1 -F0 -i patches.suse/crasher.patch
patch -p1 -F0 -i patches.suse/add-product-identifying-information-to-vmcoreinfo.patch

cp %{_sourcedir}/config-asahi-%{version} .config
make LLVM=1 rustavailable

%build
make olddefconfig prepare
make %{?_smp_mflags} ARCH=arm64 KBUILD_BUILD_USER=geeko KBUILD_BUILD_HOST=buildhost KBUILD_BUILD_VERSION=%{release} vmlinux modules dtbs Image

%install
mkdir -p %{buildroot}/boot
cp arch/arm64/boot/Image %{buildroot}/boot/Image-%{kernelrelease}
make %{?_smp_mflags} ARCH=arm64 INSTALL_MOD_PATH=%{buildroot} modules_install
make %{?_smp_mflags} ARCH=arm64 INSTALL_HDR_PATH=%{buildroot}/usr headers_install
cp System.map %{buildroot}/boot/System.map-%{kernelrelease}
cp .config %{buildroot}/boot/config-%{kernelrelease}
rm -f %{buildroot}/usr/lib/modules/%{kernelrelease}/build
mkdir -p %{buildroot}/usr/src/kernels/%{kernelrelease}
make INSTALL_PATH=. dtbs_install
install -Dpm 755 -t %{buildroot}/usr/lib/modules/%{kernelrelease}-ARCH/dtbs/ $(find dtbs/ -type f)
tar cf - --exclude SCCS --exclude BitKeeper --exclude .svn --exclude CVS --exclude .pc --exclude .hg --exclude .git --exclude=*vmlinux* --exclude=*.mod --exclude=*.o --exclude=*.ko --exclude=*.cmd --exclude=Documentation --exclude=.config.old --exclude=.missing-syscalls.d --exclude=*.s . | tar xf - -C %{buildroot}/usr/src/kernels/%{kernelrelease}

%post
if [ -x /sbin/installkernel -a -r /boot/Image-%{kernelrelease} -a -r /boot/System.map-%{kernelrelease} ]; then
cp /boot/Image-%{kernelrelease} /boot/.Image-%{kernelrelease}-rpm
cp /boot/System.map-%{kernelrelease} /boot/.System.map-%{kernelrelease}-rpm
rm -f /boot/Image-%{kernelrelease} /boot/System.map-%{kernelrelease}
/sbin/installkernel %{kernelrelease} /boot/.Image-%{kernelrelease}-rpm /boot/.System.map-%{kernelrelease}-rpm
rm -f /boot/.Image-%{kernelrelease}-rpm /boot/.System.map-%{kernelrelease}-rpm
fi

%preun
if [ -x /sbin/new-kernel-pkg ]; then
new-kernel-pkg --remove %{kernelrelease} --rminitrd --initrdfile=/boot/initramfs-%{kernelrelease}.img
elif [ -x /usr/bin/kernel-install ]; then
kernel-install remove %{kernelrelease}
fi

%postun
if [ -x /sbin/update-bootloader ]; then
/sbin/update-bootloader --remove %{kernelrelease}
fi

%files
%defattr (-, root, root)
/boot/*
/usr/lib/modules/%{kernelrelease}
/usr/lib/modules/%{kernelrelease}-ARCH/dtbs

%clean
rm -rf %{buildroot}

%package devel
Summary: Development package for building kernel modules to match the %{version} kernel
Group: System Environment/Kernel
Provides:       %name-devel = %version-%release
Provides:       multiversion(kernel)

%description devel

This package provides kernel headers and makefiles sufficient to build modules
against the %{version} kernel package.

%files devel
%defattr (-, root, root)
/usr/include
/usr/src/kernels/%{kernelrelease}

%changelog

