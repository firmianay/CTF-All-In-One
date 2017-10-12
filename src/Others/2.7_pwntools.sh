#!/usr/bin/env bash

V = 2.29   # binutils version
ARCH = arm # target architecture

cd /tmp
wget -nc https://ftp.gnu.org/gnu/binutils/binutils-$V.tar.xz
wget -nc https://ftp.gnu.org/gnu/binutils/binutils-$V.tar.xz.sig

# gpg --keyserver keys.gnupg.net --recv-keys C3126D3B4AE55E93
# gpg --verify binutils-$V.tar.xz.sig

tar xf binutils-$V.tar.xz

mkdir binutils-build
cd binutils-build

export AR=ar
export AS=as

../binutils-$V/configure \
    --prefix=/usr/local \
    --target=$ARCH-unknown-linux-gnu \
    --disable-static \
    --disable-multilib \
    --disable-werror \
    --disable-nls

make
sudo make install
