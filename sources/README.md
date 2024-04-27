# sources
Files here should be in the SOURCES directory of rpmbuild. You may run `rpm --eval %_sourcedir` to determine the path. Just refer to the spec files for the expected filenames. 

### Kernel

#### Kernel source
https://github.com/AsahiLinux/linux

#### Speaker enablement patches
10-speakers-enable-part1.patch: https://github.com/AsahiLinux/linux/commit/385ea7b5023486aba7919cec8b6b3f6a843a1013.patch
10-speakers-enable-part2.patch: https://github.com/AsahiLinux/linux/commit/6a24102c06c95951ab992e2d41336cc6d4bfdf23.patch

**NOTE: When enabling the speakers, make sure to have the appropriate lsp-plugins version. More details can be found in the patch.**

#### openSUSE specific patches
https://github.com/openSUSE/kernel-source

#### Reference .config file
sources/config-asahi-6.8.6

### alsa-config-ucm-asahi / asahi-audio / asahi-fwextract / asahi-scripts / m1n1 / speakersafetyd / u-boot
https://github.com/AsahiLinux

#### update-m1n1 config file
sources/update-m1n1.sysconfig

### asahi-bless
https://github.com/WhatAmISupposedToPutHere/asahi-nvram

### bankstown-lv2
https://github.com/chadmed/bankstown/

### mesa
https://gitlab.freedesktop.org/asahi/mesa
sources/n_add-Mesa-headers-again.patch
 
