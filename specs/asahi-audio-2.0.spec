Name:           asahi-audio
Version:        2.0
Release:        2
Summary:        Linux userspace audio configurations for Apple Silicon

License:        MIT
URL:            https://github.com/AsahiLinux/asahi-audio
Source0:        %{name}-%{version}.tar.gz
Requires:       wireplumber >= 0.5.0
Requires:       pipewire >= 1.0.0
Requires:       bankstown-lv2 >= 1.1.0
Requires:       lsp-plugins >= 1.0.20
Requires:       speakersafetyd 
Requires:       kernel-asahi
Provides:       asahi-audio = %{version}-%{release}
Obsoletes:      asahi-audio < 2.0
BuildArch:      noarch

%description
Linux userspace audio configrations for Apple Silicon

# aarch64 as a fallback of _arch in case
# /usr/lib/rpm/platform/*/macros was not included.
%define _arch %{?_arch:aarch64}
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}

%prep
%setup -q -n %{name}-%{version}

%build
make %{?_smp_mflags} all

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%defattr (-, root, root)
/usr/share/asahi-audio
/usr/share/wireplumber/wireplumber.conf.d/99-asahi.conf
/usr/share/wireplumber/scripts/device/asahi-limit-volume.lua
/usr/share/pipewire/pipewire.conf.d/99-asahi.conf
/usr/share/pipewire/pipewire-pulse.conf.d/99-asahi.conf

%changelog
