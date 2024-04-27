Name:           uboot-asahi
Version:        2023.07.02
Release:        5
Summary:        U-Boot for Apple Silicon Macs
License:        GPLv3+
URL:            https://github.com/AsahiLinux
BuildArch:      aarch64
%define ubootasahirel 4
%define debug_package %{nil}
%define uboot_commit_id asahi-v%{version}-%{ubootasahirel}

Source0:        https://github.com/AsahiLinux/u-boot/archive/%{uboot_commit_id}.tar.gz

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  ImageMagick
BuildRequires:  make
BuildRequires:  libopenssl-devel


Provides: /usr/lib/asahi-boot/u-boot-nodtb.bin

%description
U-Boot for Apple Silicon Macs

%prep
%setup -b 0 -n u-boot-asahi-v%{version}-%{ubootasahirel}
make %{_builddir}/u-boot-%{uboot_commit_id} apple_m1_defconfig

%build
%make_build HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE=""

%install
install -Dpm0644 -t %{buildroot}/%{_datadir}/uboot/apple_m1 u-boot-nodtb.bin

%files
%license Licenses/*
%{_datadir}/uboot/apple_m1/u-boot-nodtb.bin

%changelog
