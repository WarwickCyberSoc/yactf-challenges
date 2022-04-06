#include <stdio.h>
#include <unistd.h>

void main() {

    char mald[] = "\x48\x8B\x04\x24\xC3";
    // mov rax, [rsp];
    // ret;

    long ret = syscall(548, mald, sizeof(mald));
    
    printf("return value: %p\n", ret);

}
