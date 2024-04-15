Name:           asahi-scripts
Version:        20240411
Release:        1
Summary:        Miscellaneous scripts for Asahi Linux

License:        MIT
URL:            https://github.com/AsahiLinux/asahi-scripts
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  systemd-rpm-macros

Requires:       bash
Requires:       dracut
Requires:       coreutils
Requires:       sed
Requires:       tar
Requires:       m1n1
Requires:       uboot-asahi
Requires:       asahi-fwextract

BuildArch:      noarch

%description
This package contains miscellaneous admin scripts for the Asahi Linux reference
distro.

%prep
%setup -n asahi-scripts-%{version}

%install
make DESTDIR=%{buildroot} PREFIX=/usr install
make DESTDIR=%{buildroot} PREFIX=/usr DRACUT_CONF_DIR=/usr/lib/dracut.conf.d install-dracut

%files
%license LICENSE
/etc/m1n1.conf
/usr/bin/update-m1n1
/usr/bin/asahi-fwupdate
/usr/bin/asahi-diagnose
/usr/share/asahi-scripts/functions.sh
/usr/lib/dracut.conf.d/10-asahi.conf
/usr/lib/dracut/modules.d/99asahi-firmware/module-setup.sh
/usr/lib/dracut/modules.d/99asahi-firmware/install-asahi-firmware.sh
/usr/lib/dracut/modules.d/99asahi-firmware/load-asahi-firmware.sh
/usr/lib/firmware/vendor

%changelog
