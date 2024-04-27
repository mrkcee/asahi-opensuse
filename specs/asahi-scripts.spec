Name:           asahi-scripts
Version:        20240411
Release:        2
Summary:        Miscellaneous scripts for Asahi Linux

License:        MIT
URL:            https://github.com/AsahiLinux/asahi-scripts
Vendor:         Asahi Linux Contributors
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        update-m1n1.sysconfig

Requires:       bash
Requires:       dracut
Requires:       coreutils
Requires:       sed
Requires:       tar
Requires:       m1n1
Requires:       uboot-asahi
Requires:       asahi-fwextract

BuildArch:      noarch

Provides:       %{name} = %{version}-%{release}
Obsoletes:      asahi-scripts < 20240411-2

%description
This package contains miscellaneous admin scripts for the Asahi Linux reference
distro.

%package -n     asahi-fwupdate
Summary:        Asahi Linux firmware extractor

Requires:       %{name} = %{version}-%{release}
Provides:       asahi-fwupdate = %{version}-%{release}

%description -n asahi-fwupdate
Asahi Linux firmware updater.

%package -n     update-m1n1
Summary:        Keep m1n1 up to date

Requires:       %{name} = %{version}-%{release}

Requires:       bash
Requires:       gzip
Requires:       m1n1
Requires:       uboot-asahi

%description -n update-m1n1
Keep m1n1 up to date on Apple Silicon systems

%prep
%setup -n asahi-scripts-%{version}

%install
make DESTDIR=%{buildroot} PREFIX=%{_prefix} install
make DESTDIR=%{buildroot} PREFIX=%{_prefix} DRACUT_CONF_DIR=%{_prefix}/lib/dracut.conf.d install-dracut
install -Dpm0644 %SOURCE1 %{buildroot}/%{_sysconfdir}/sysconfig/update-m1n1

%transfiletriggerin -n asahi-fwupdate -- %{_bindir}/asahi-fwupdate %{_bindir}/asahi-fwextract
%{_bindir}/asahi-fwupdate || :

# This needs to be a separate trigger because we can't use python3_sitearch here
%transfiletriggerin -n asahi-fwupdate -- /usr/lib/python
grep -q 'asahi_firmware' && %{_bindir}/asahi-fwupdate || :

# We can't use _libdir here because it gets incorrectly expanded to /usr/lib
%transfiletriggerin -n update-m1n1 -- /usr/lib/m1n1 /usr/lib64/m1n1 /usr/share/uboot/apple_m1 /boot/dtb-
%{_bindir}/update-m1n1 || :

%files -n asahi-fwupdate
%license LICENSE
%{_bindir}/asahi-fwupdate

%files -n update-m1n1
%license LICENSE
%{_sysconfdir}/m1n1.conf
%{_bindir}/update-m1n1
%{_sysconfdir}/sysconfig/update-m1n1

%files
%{_bindir}/asahi-diagnose
%{_datadir}/asahi-scripts/functions.sh
%{_prefix}/lib/dracut.conf.d/10-asahi.conf
%{_prefix}/lib/dracut/modules.d/99asahi-firmware/
%{_prefix}/lib/firmware/vendor

%changelog
