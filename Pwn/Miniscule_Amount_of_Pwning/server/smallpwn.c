// gcc -no-pie smallpwn.c -o smallpwn
main(){gets(__builtin_frame_address(0));}
