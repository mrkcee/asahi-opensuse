Name:           speakersafetyd
Version:        0.1.9
Release:        2
Summary:        Speaker userspace daemon for Apple Silicon

License:        MIT
URL:            https://github.com/AsahiLinux/speakersafetyd
Source0:        %{name}-%{version}.tar.gz
Vendor:         asahi-opensuse

# TODO: BuildRequires for rust
#BuildRequires:  rust
BuildRequires:  alsa-devel

%description
speakersafetyd is a userspace daemon written in Rust that implements an analogue of the Texas Instruments Smart Amp speaker protection model.

# aarch64 as a fallback of _arch in case
# /usr/lib/rpm/platform/*/macros was not included.
%define _arch %{?_arch:aarch64}
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}

%prep
%setup -q

%build
make %{?_smp_mflags} all

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} UNITDIR=usr/lib/systemd/system UDEVDIR=%{_udevrulesdir} install

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, root)
%license LICENSE
%{_bindir}/speakersafetyd
/usr/lib/udev/rules.d/95-speakersafetyd.rules
/usr/lib/systemd/system/speakersafetyd.service
%{_datadir}/speakersafetyd/apple
/var/lib/speakersafetyd/blackbox
/usr/lib/tmpfiles.d/speakersafetyd.conf

%changelog
