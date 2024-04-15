Name:           asahi-fwextract
Version:        0.7.1
Release:        1
Summary:        Miscellaneous scripts for Asahi Linux

License:        MIT
URL:            https://github.com/AsahiLinux/asahi-installer
Source0:        asahi-installer-0.7.1.tar.gz

BuildArch:      noarch

%description
This package contains miscellaneous admin scripts for the Asahi Linux reference
distro.

%prep
%setup -n asahi-installer-%{version}

%build
%py3_build

%install
%py3_install

%files
%license LICENSE
/usr/bin/asahi-fwextract
%{python3_sitelib}/asahi_firmware/
%{python3_sitelib}/asahi_firmware-*.egg-info/

%changelog
