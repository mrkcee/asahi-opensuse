Name:           m1n1
Version:        1.4.11
Release:        3
Summary:        Bootloader and experimentation playground for Apple Silicon

# m1n1 proper is MIT licensed, but it relies on a number of vendored projects
# See the "License" section in README.md for the breakdown
License:        MIT and CC0 and BSD and OFL and zlib
URL:            https://github.com/AsahiLinux/m1n1
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Vendor:         asahi-opensuse

%ifarch aarch64
# On aarch64 do a native build
BuildRequires:  gcc
%global buildflags RELEASE=1 ARCH=
%else
# By default m1n1 does a cross build
BuildRequires:  gcc-aarch64-linux-gnu
%global buildflags RELEASE=1
%endif
BuildRequires:  make

BuildRequires:  ImageMagick
BuildRequires:  zopfli

# For the udev rule
BuildRequires:  systemd-rpm-macros

# These are bundled, modified and statically linked into m1n1
Provides:       bundled(arm-trusted-firmware)
Provides:       bundled(dwc3)
Provides:       bundled(dlmalloc)
Provides:       bundled(PDCLib)
Provides:       bundled(libfdt)
Provides:       bundled(minilzlib)
Provides:       bundled(tinf)

%description
m1n1 is the bootloader developed by the Asahi Linux project to bridge the Apple
(XNU) boot ecosystem to the Linux boot ecosystem.

%package        tools
Summary:        Developer tools for m1n1
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       python3dist(construct)
Requires:       python3dist(pyserial)
Requires:       systemd-udev
BuildArch:      noarch

%description    tools
This package contains various developer tools for m1n1.

%prep
%setup -n %{name}-%{version}

%build
%make_build %{buildflags}

%install
install -Dpm0644 -t %{buildroot}/%{_libdir}/%{name} build/%{name}.{bin,macho}
install -Ddpm0755 %{buildroot}%{_libexecdir}/%{name}
install -Dpm0644 -t %{buildroot}%{_udevrulesdir} udev/80-m1n1.rules

%files
%license LICENSE 3rdparty_licenses/LICENSE.*
%doc README.md
%{_libdir}/%{name}

%files tools
%license LICENSE 3rdparty_licenses/LICENSE.*
%{_udevrulesdir}/80-m1n1.rules
%{_libexecdir}/%{name}

%changelog
