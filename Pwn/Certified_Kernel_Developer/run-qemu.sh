#!/bin/sh

qemu-system-x86_64 \
-m 128M \
-kernel ./bzImage \
-initrd  ./initramfs.cpio.gz \
-append "root=/dev/ram rw console=ttyS0 oops=panic panic=1 quiet kaslr" \
-cpu qemu64,+smep,+smap \
-smp 2 \
-s  \
-netdev user,id=t0, -device e1000,netdev=t0,id=nic0 \
-nographic \
-monitor /dev/null \
