Name:           bankstown-lv2
Version:        1.1.0
Release:        1
Summary:        A barebones bass enhancer

License:        MIT
URL:            https://github.com/chadmed/bankstown
Source0:        bankstown-lv2-%{version}.tar.gz

%description
A barebones bass enhancer

# aarch64 as a fallback of _arch in case
# /usr/lib/rpm/platform/*/macros was not included.
%define _arch %{?_arch:aarch64}
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}

%prep
%setup -q -n bankstown-%{version}

%build
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, root)
/usr/lib64/lv2/bankstown.lv2/bankstown.so
/usr/lib64/lv2/bankstown.lv2/bankstown.ttl
/usr/lib64/lv2/bankstown.lv2/manifest.ttl

%changelog
