%define _rcver 6.6
%define _asahirel 16
%define _commit_id asahi-%{_rcver}-%{_asahirel}
%define _rpm_ver %{_rcver}.3

# how the kernel release string (uname -r) should look like
%define kernelrelease %{_rcver}.3-asahi

Name: kernel-asahi
Summary: The Linux Kernel
Version: 6.6.3
Release: 1
License: GPL
Group: System Environment/Kernel
Vendor: The Linux Community
URL: https://www.kernel.org
Source0: https://github.com/AsahiLinux/linux/archive/refs/tags/%{_commit_id}.tar.gz
Source1: config-%{_commit_id}
# Speaker enablement patches
Patch0: 10-speakers-enable-part1.patch
Patch1: 10-speakers-enable-part2.patch
#Patch2: patch-6.6.3.xz
BuildRequires: bc binutils bison dwarves
BuildRequires: (elfutils-libelf-devel or libelf-devel) flex
BuildRequires: gcc make openssl openssl-devel perl python3 rsync
# TODO: add BuildRequires for rustc bindgen when installed via rustup
#BuildRequires: rust rust-bindgen
Provides:       %name-%version-%_asahirel
Provides:       %{name}_%_target_cpu = %version-%_asahirel
Provides:       kernel-base = %version-%_asahirel
Provides:       kernel = %version-%_asahirel
Provides:       multiversion(kernel)
Obsoletes:      %name-base < 3.1
Conflicts:      filesystem < 16
Obsoletes:      microcode_ctl < 1.18
Requires(post): kmod-zstd
%description
The Linux Kernel, the operating system core itself

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
tar xzf %{_sourcedir}/patch-6.6.3.tar.gz
rm patch-6.6.3/6.6.1-015-Bluetooth-hci_bcm4377-Mark-bcm4378-bcm4387-as-B.patch 
rm patch-6.6.3/6.6.2-532-regmap-prevent-noinc-writes-from-clobbering-cac.patch
rm patch-6.6.3/6.6.2-475-xhci-Loosen-RPM-as-default-policy-to-cover-for-.patch
rm patch-6.6.3/6.6.3-287-regmap-Ensure-range-selector-registers-are-upda.patch
rm patch-6.6.3/6.6.3-411-xhci-Enable-RPM-on-controllers-that-support-low.patch
for f in ./patch-6.6.3/*.patch; do
	patch -p1 -F0 -i $f
done

cp %{_sourcedir}/config-%{_commit_id} .config
make LLVM=1 rustavailable

%build
make olddefconfig prepare
make %{?_smp_mflags} ARCH=arm64 KBUILD_BUILD_USER=geeko KBUILD_BUILD_HOST=buildhost KBUILD_BUILD_VERSION=%{release} vmlinux modules dtbs Image

%install
mkdir -p %{buildroot}/boot
cp arch/arm64/boot/Image %{buildroot}/boot/Image-%{kernelrelease}
make %{?_smp_mflags} ARCH=arm64 INSTALL_MOD_PATH=%{buildroot} MODLIB='$(INSTALL_MOD_PATH)/usr/lib/modules/%{kernelrelease}' modules_install
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
Summary: Development package for building kernel modules to match the %{_rpm_ver} kernel
Group: System Environment/Kernel
Provides:       %name-devel = %version-%_asahirel
Provides:       multiversion(kernel)

%description devel

This package provides kernel headers and makefiles sufficient to build modules
against the %{_rpm_ver} kernel package.

%files devel
%defattr (-, root, root)
/usr/include
/usr/src/kernels/%{kernelrelease}

%changelog

