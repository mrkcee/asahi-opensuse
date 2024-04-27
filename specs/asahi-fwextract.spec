Name:           asahi-fwextract
Version:        0.7.1
Release:        3
Summary:        Asahi Linux firmware extractor

License:        MIT
URL:            https://github.com/AsahiLinux/asahi-installer
Vendor:         asahi-opensuse
Source0:        asahi-installer-0.7.1.tar.gz

BuildArch:      noarch

Provides:       asahi-fwextract = %{version}-%{release}
Obsoletes:      asahi-fwextract < 0.7.1

%description
Asahi Linux firmware extractor

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
