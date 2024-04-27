%define _rcver 6.8.6
%define _asahirel 3
%define _tag_id asahi-%{_rcver}-%{_asahirel}

Name: kernel-asahi
Summary: The Linux Kernel
Version: 6.8.6
Release: 4
License: GPL
Group: System Environment/Kernel
Vendor: The Linux Community
URL: https://www.kernel.org
Source0: https://github.com/AsahiLinux/linux/archive/refs/tags/%{_tag_id}.tar.gz
Source1: config-asahi-%{version}-%{_asahirel}
# Compressed patch files from kernel-source repo
# 
# Speaker enablement patches
Patch0: 10-speakers-enable-part1.patch
Patch1: 10-speakers-enable-part2.patch
Requires(pre):  suse-kernel-rpm-scriptlets
Requires(post): suse-kernel-rpm-scriptlets
Requires:       suse-kernel-rpm-scriptlets
Requires(preun): suse-kernel-rpm-scriptlets
Requires(postun): suse-kernel-rpm-scriptlets
BuildRequires: bash-sh bc binutils bison dwarves
BuildRequires: (elfutils-libelf-devel or libelf-devel) flex
BuildRequires: gcc make openssl openssl-devel perl python3 rsync
# TODO: add BuildRequires for rustc bindgen when installed via rustup
#BuildRequires: rust rust-bindgen
Provides:       %{name} = %{version}-%{release}
Provides:       %{name}-%{version}-%{release}
Provides:       %{name}_%{_target_cpu} = %{version}-%{release}
Provides:       kernel-base = %{version}-%{release}
Provides:       %{name}-base = %{version}-%{release}
Provides:       kernel = %{version}-%{release}
Provides:       multiversion(kernel)
Conflicts:      filesystem < 16
Obsoletes:      microcode_ctl < 1.18
BuildRequires:  zstd
Requires(post): modutils
Requires(post): kmod-zstd
Requires(post): perl-Bootloader >= 0.4.15
Requires(post): dracut
Requires(post): distribution-release
%description
The standard kernel for both uniprocessor and multiprocessor systems.

# how the kernel release string (uname -r) should look like
%define unametag -asahi-%{_asahirel}-%{release}
%define kernelrelease %{version}%{unametag}

%define dtbdir /boot/dtb-%{kernelrelease}

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
%setup -n linux-%{_tag_id} -q
%patch 0 -p1
%patch 1 -p1

# Remove patches that conflict with Asahi-specific changes or were applied already
# Some will have to be manually applied/merged

# for f in `ls -v ./patches.kernel.org/*.patch`; do
#	patch -p1 -F0 -i $f
# done

# Apply RPM-related patches
tar xzf %{_sourcedir}/patches-rpmify.tar.gz
for f in ./patches.rpmify/*.patch; do
	patch -p1 -F0 -i $f
done

# Apply SUSE-specific patches
tar xzf %{_sourcedir}/patches-suse.tar.gz
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
patch -p1 -F0 -i patches.suse/Revert-btrfs-remove-code-for-inode_cache-and-recover.patch
patch -p1 -F0 -i patches.suse/b43-missing-firmware-info.patch
patch -p1 -F0 -i patches.suse/crasher.patch
patch -p1 -F0 -i patches.suse/add-product-identifying-information-to-vmcoreinfo.patch

echo %{unametag} > localversion.05-asahi

cp %{_sourcedir}/config-asahi-%{version}-%{_asahirel} .config
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
install -Dpm 755 -t %{buildroot}%{dtbdir}/apple/ $(find dtbs/ -type f)
tar cf - --exclude SCCS --exclude BitKeeper --exclude .svn --exclude CVS --exclude .pc --exclude .hg --exclude .git --exclude=*vmlinux* --exclude=*.mod --exclude=*.o --exclude=*.ko --exclude=*.cmd --exclude=Documentation --exclude=.config.old --exclude=.missing-syscalls.d --exclude=*.s . | tar xf - -C %{buildroot}/usr/src/kernels/%{kernelrelease}

%pre

%post
if [ -x /usr/lib/module-init-tools/weak-modules2 ]; then
	/usr/lib/module-init-tools/weak-modules2 --add-kernel "%{kernelrelease}"
fi
if [ -x /usr/lib/bootloader/bootloader_entry ]; then
	/usr/lib/bootloader/bootloader_entry add "asahi" "%{kernelrelease}" "Image-%{kernelrelease}" "initrd-%{kernelrelease}"
fi

%posttrans

%preun

%postun
if [ -x /usr/lib/module-init-tools/weak-modules2 ]; then
	/usr/lib/module-init-tools/weak-modules2 --remove-kernel "%{kernelrelease}"
fi
if [ -x /usr/lib/bootloader/bootloader_entry ]; then
	/usr/lib/bootloader/bootloader_entry remove "asahi" "%{kernelrelease}" "Image-%{kernelrelease}" "initrd-%{kernelrelease}"
fi

%files
%defattr (-, root, root)
/boot/config-%{kernelrelease}
/boot/Image-%{kernelrelease}
/boot/System.map-%{kernelrelease}
/usr/lib/modules/%{kernelrelease}

%package -n dtb-apple
Summary:        Apple Silicon SOC based arm64 systems
Group:          System/Boot
Provides:       multiversion(dtb)
Requires(post): coreutils

%description -n dtb-apple
Device Tree files for Apple Silicon SOC based arm64 systems

%post -n dtb-apple
cd /boot
# If /boot/dtb is a symlink, remove it, so that we can replace it.
[ -d dtb ] && [ -L dtb ] && rm -f dtb
# Unless /boot/dtb exists as real directory, create a symlink.
[ -d dtb ] || ln -sf dtb-%{kernelrelease} dtb

%files -n dtb-apple
%defattr(-,root,root)
%ghost /boot/dtb
%dir %{dtbdir}
%dir %{dtbdir}/apple
%{dtbdir}/apple/*.dtb

%package devel
Summary: Development package for building kernel modules to match the %{version} asahi kernel
Group: System Environment/Kernel
Provides:       %{name}-devel = %{version}-%{release}
Provides:       multiversion(kernel)

%description devel

This package provides kernel headers and makefiles sufficient to build modules
against the %{version} asahi kernel package.

%files devel
%defattr (-, root, root)
/usr/include
/usr/src/kernels/%{kernelrelease}

%changelog

