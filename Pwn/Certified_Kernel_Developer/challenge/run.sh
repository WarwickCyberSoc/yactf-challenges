#!/bin/sh
cd /home/ctf
qemu-system-x86_64 \
        -kernel ./bzImage \
        -initrd ./initramfs.cpio.gz \
        -monitor /dev/null \
        -nographic -append "console=ttyS0 kaslr"