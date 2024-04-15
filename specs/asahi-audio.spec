Name:           asahi-audio
Version:        1.8
Release:        1
Summary:        Linux userspace audio configurations for Apple Silicon

License:        MIT
URL:            https://github.com/AsahiLinux/chadmed
Source0:        %{name}-%{version}.tar.gz
Provides:       asahi-audio = %{version}
Obsoletes:      asahi-audio <= 1.8

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
/usr/share/wireplumber/policy.lua.d/85-asahi-policy.lua
/usr/share/wireplumber/main.lua.d/85-asahi.lua
/usr/share/wireplumber/scripts/policy-asahi.lua
/usr/share/pipewire/pipewire.conf.d/99-asahi.conf
/usr/share/pipewire/pipewire-pulse.conf.d/99-asahi.conf

%changelog
