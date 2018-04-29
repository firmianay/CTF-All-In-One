#!/bin/bash

cd ./initramfs/
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../initramfs.cpio.gz
