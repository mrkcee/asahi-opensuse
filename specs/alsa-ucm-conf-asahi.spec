Name:           alsa-ucm-conf-asahi
Version:        5
Release:        1
Summary:        ALSA Use Case Manager configuration (and topologies) for Apple silicon devices

License:        MIT
URL:            https://asahilinux.org
Vendor:         Asahi Linux Contributors
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

%description
ALSA Use Case Manager configuration (and topologies) for Apple silicon devices

# aarch64 as a fallback of _arch in case
# /usr/lib/rpm/platform/*/macros was not included.
%define _arch %{?_arch:aarch64}
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}

%prep
%setup -q -n %{name}-%{version}

%build

%install
mkdir -p %{buildroot}%{_datadir}/alsa/ucm2/conf.d
cp -av ucm2/conf.d/macaudio %{buildroot}%{_datadir}/alsa/ucm2/conf.d

%files
%defattr (-, root, root)
%{_datadir}/alsa/ucm2/conf.d/macaudio

%changelog
