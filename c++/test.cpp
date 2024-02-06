#include <iostream>
#include <ncurses.h>
#include <unistd.h> // for usleep

using namespace std;

bool gameover;
const int width = 20;
const int height = 10;
int x, y, fruitX, fruitY, score;
int tailX[100], tailY[100];
int nTail;
enum eDirection { STOP = 0, LEFT, RIGHT, UP, DOWN };
eDirection dir;

void Setup() {
    initscr();
    clear();
    noecho();
    cbreak();
    keypad(stdscr, TRUE);
    curs_set(0);

    gameover = false;
    dir = STOP;
    x = width / 2;
    y = height / 2;
    fruitX = rand() % width;
    fruitY = rand() % height;
    score = 0;
}

void Draw() {
    clear();
    for (int i = 0; i < width + 2; i++)
        printw("#");
    printw("\n");

    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            if (j == 0)
                printw("#"); // left wall

            if (i == y && j == x)
                printw("O"); // snake head
            else if (i == fruitY && j == fruitX)
                printw("F"); // fruit
            else {
                bool print = false;
                for (int k = 0; k < nTail; k++) {
                    if (tailX[k] == j && tailY[k] == i) {
                        printw("o"); // snake tail
                        print = true;
                    }
                }
                if (!print)
                    printw(" ");
            }

            if (j == width - 1)
                printw("#"); // right wall
        }
        printw("\n");
    }

    for (int i = 0; i < width + 2; i++)
        printw("#");
    printw("\n");
    printw("Score:%d\n", score);

    refresh();
}

void Input() {
    int key = getch();
    switch (key) {
    case 'a':
        dir = LEFT;
        break;
    case 'd':
        dir = RIGHT;
        break;
    case 'w':
        dir = UP;
        break;
    case 's':
        dir = DOWN;
        break;
    case 'x':
        gameover = true;
        break;
    }
}

void Algorithm() {
    int prevX = tailX[0];
    int prevY = tailY[0];
    int prev2X, prev2Y;
    tailX[0] = x;
    tailY[0] = y;
    for (int i = 1; i < nTail; i++) {
        prev2X = tailX[i];
        prev2Y = tailY[i];
        tailX[i] = prevX;
        tailY[i] = prevY;
        prevX = prev2X;
        prevY = prev2Y;
    }
    switch (dir) {
    case LEFT:
        x--;
        break;
    case RIGHT:
        x++;
        break;
    case UP:
        y--;
        break;
    case DOWN:
        y++;
        break;
    default:
        break;
    }
    if (x >= width)
        x = 0;
    else if (x < 0)
        x = width - 1;

    if (y >= height)
        y = 0;
    else if (y < 0)
        y = height - 1;

    for (int i = 0; i < nTail; i++)
        if (tailX[i] == x && tailY[i] == y)
            gameover = true;

    if (x == fruitX && y == fruitY) {
        score += 10;
        fruitX = rand() % width;
        fruitY = rand() % height;
        nTail++;
    }
}

int main() {
    Setup();
    while (!gameover) {
        Draw();
        Input();
        Algorithm();
        usleep(100000); // sleep for 10 milliseconds
    }

    endwin(); // close ncurses window
    return 0;
}