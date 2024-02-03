#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <iostream>
#include <unistd.h>

const int ballSize = 20;
const int screenWidth = 800;
const int screenHeight = 600;
const int initialX = screenWidth / 2;
const int initialY = screenHeight / 2;

int main() {
    Display* display = XOpenDisplay(nullptr);
    if (!display) {
        std::cerr << "Unable to open display" << std::endl;
        return 1;
    }

    int screen = DefaultScreen(display);
    Window root = RootWindow(display, screen);

    Window window = XCreateSimpleWindow(display, root, 0, 0, screenWidth, screenHeight, 1, BlackPixel(display, screen), WhitePixel(display, screen));
    XSelectInput(display, window, ExposureMask);
    XMapWindow(display, window);

    XStoreName(display, window, "Bouncing Ball");

    GC gc = XCreateGC(display, window, 0, nullptr);

    int ballX = initialX;
    int ballY = initialY;
    int xDirection = 1;
    int yDirection = 1;

    XEvent event;
    bool quit = false;

    while (!quit) {
        while (XPending(display) > 0) {
            XNextEvent(display, &event);

            if (event.type == Expose) {
                XClearWindow(display, window);
                XFillArc(display, window, gc, ballX, ballY, ballSize, ballSize, 0, 360 * 64);
            }
        }

        // Update ball position
        ballX += xDirection;
        ballY += yDirection;

        // Bounce off the walls
        if (ballX <= 0 || ballX >= (screenWidth - ballSize))
            xDirection *= -1;

        if (ballY <= 0 || ballY >= (screenHeight - ballSize))
            yDirection *= -1;

        // Pause for a short time to control ball speed
        usleep(10000);

        // Redraw the window
        XClearWindow(display, window);
        XFillArc(display, window, gc, ballX, ballY, ballSize, ballSize, 0, 360 * 64);
    }

    XDestroyWindow(display, window);
    XCloseDisplay(display);

    return 0;
}