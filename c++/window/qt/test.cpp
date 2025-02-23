#include <QApplication>
#include <QWidget>
#include <QPushButton>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv); // Create the application object

    // Create a main window
    QWidget window;
    window.setWindowTitle("Qt Example");

    // Create a button
    QPushButton *button = new QPushButton("Click me!", &window);
    button->setGeometry(10, 10, 100, 30); // Set button size and position

    // Connect a slot to handle button click
    QObject::connect(button, &QPushButton::clicked, [&](){
        button->setText("Clicked!"); // Change button text when clicked
    });

    window.resize(300, 200); // Resize the window
    window.show(); // Show the window

    return app.exec(); // Enter the application's main event loop
}
