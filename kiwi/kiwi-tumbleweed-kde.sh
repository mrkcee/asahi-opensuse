#!/bin/sh

distro=Tumbleweed
edition=KDE
sudo rm -rf ./outdir-$distro-$edition
sudo kiwi-ng --debug --type=oem --profile=$distro-$edition --color-output system build --description ./ --target-dir ./outdir-$distro-$edition
