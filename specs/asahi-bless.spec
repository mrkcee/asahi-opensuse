Name:           asahi-bless
Version:        0.3.0
Release:        1
Summary:        Tool to select active boot partition on Apple Silicon

License:        MIT
URL:            https://crates.io/crates/asahi-bless
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  cargo-packaging

%description
A tool to select active boot partition on Apple Silicon

# aarch64 as a fallback of _arch in case
# /usr/lib/rpm/platform/*/macros was not included.
%define _arch %{?_arch:aarch64}
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}

%prep
%setup -n asahi-nvram-%{name}-%{version}

%build
%cargo_build

%install
cd asahi-bless
%cargo_install

%files
/usr/bin/asahi-bless

%changelog
