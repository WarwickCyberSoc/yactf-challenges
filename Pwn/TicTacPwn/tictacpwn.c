#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include "ANSI-color-codes.h"

// gcc -m32 tictacpwn.c -o tictacpwn

void saveScore(char name[], char file[], int winner) {
    FILE *fptr;
    char c;

    if((fptr=fopen(file,"a")) == NULL)
    {
        printf("Error writing to file!");   
    }
    else
    {
        if(winner == 2)
        {
            fprintf(fptr,"%s won against the AI!\n", name);
        }
        else
        {
            fprintf(fptr,"%s lost against the AI!\n", name);
        }
        fclose(fptr);
    }

    if((fptr=fopen(file,"r")) == NULL)
    {
        printf("Error reading the file!");   
        return;
    }

    printf("Leaderboard:\n");
    while ((c = getc(fptr)) != EOF)
        putchar(c);

    fclose(fptr);
}

#define CROSS REDB " X " COLOR_RESET
#define CIRCLE BLUB " O " COLOR_RESET
#define BORDER WHTB "   " COLOR_RESET
#define EMPTY "   "

// circle = 2
// cross = 1
// empty = 0

void setup()
{
    srand(time(0));
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}


int printBoard(int board[9])
{
    printf("\n");
    for(int square = 0; square < 9; square++)
    {
        if(square % 3 == 0)
        {
            printf(EMPTY);
        }

        printf(board[square] == 0 ? EMPTY : (board[square] == 1 ? CROSS : CIRCLE));
        if(square == 2 || square == 5)
        {
            printf("\n" EMPTY BORDER BORDER BORDER BORDER BORDER "\n");
        }
        else if(square != 8)
        {
            printf(BORDER);
        }
        else
        {
            printf("\n\n");
        }
    }
}

int getAIMove(int board[9])
{
    int move;
    do {
        move = rand() % 9;
    } while (board[move] != 0);
    return move;
}

int checkWin(int board[9])
{
    for(int player = 1; player <= 2; player++)
    {
        if(
            (board[0] == player && board[1] == player && board[2] == player) || 
            (board[3] == player && board[4] == player && board[5] == player) || 
            (board[6] == player && board[7] == player && board[8] == player) ||
            (board[0] == player && board[3] == player && board[6] == player) || 
            (board[1] == player && board[4] == player && board[7] == player) || 
            (board[2] == player && board[5] == player && board[9] == player) ||
            (board[0] == player && board[4] == player && board[8] == player) || 
            (board[2] == player && board[4] == player && board[6] == player)
        )
        {
            return player;
        }
    }

    return 0;
}

int main(int argc, char *argv[]) {
    setup();

    int board[9] = {0,0,0,0,0,0,0,0,0};
    int winner = 0;
    int move;

    char name[32];
    char leaderboardFile[32] = "./leaderboard.txt";

    for(int turn = 0; turn < 9; turn++)
    {
        printBoard(board);

        if(turn % 2 == 0)
        {
            // AI turn
            printf("The AI is thinking...\n");
            sleep(1);
            move = getAIMove(board);

            board[move] = 1;
        }
        else
        {
            move = 0;

            // Player turn
            while(1)
            {
                printf("Please select a square to play on (1-9): ");
                scanf("%d", &move);
                getchar();
                if(move < 1 || move > 9 || board[move - 1] != 0)
                {
                    printf("You can't play there!\n");
                    continue;
                }
                move--;

                board[move] = 2;
                break;
            }
        }
        
        winner = checkWin(board);

        if(winner == 0 && turn == 8)
        {
            printf("\nNo one won...");
            exit(0);
        }
        else if(winner != 0)
        {
            break;
        }
    }

    printBoard(board);
    
    printf("\n%s won!\n", winner == 1 ? "The AI" : "You");

    printf("\nWhat is your name?\n> ");
    fgets(name, 64, stdin);
    name[strcspn(name, "\n")] = 0;

    saveScore(name, leaderboardFile, winner);
}