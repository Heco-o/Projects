#include <SFML/Graphics.hpp>
#include <vector>
#include <thread>

// Function to create a new window
void createNewWindow() {
    sf::RenderWindow window(sf::VideoMode(200, 200), "New Window");
    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
            }
        }
    }
}

int main() {
    std::vector<std::thread> threads;

    // Create the main window
    sf::RenderWindow mainWindow(sf::VideoMode(400, 400), "Main Window");

    // Create a button
    sf::RectangleShape button(sf::Vector2f(100, 50));
    button.setFillColor(sf::Color::Green);
    button.setPosition(150, 175);

    // Create a text for the button
    sf::Font font;
    if (!font.loadFromFile("arial.ttf")) {
        // Error handling
        return EXIT_FAILURE;
    }
    sf::Text buttonText("Create New Window", font, 16);
    buttonText.setPosition(155, 185);

    while (mainWindow.isOpen()) {
        sf::Event event;
        while (mainWindow.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                mainWindow.close();
            }
            if (event.type == sf::Event::MouseButtonPressed) {
                if (event.mouseButton.button == sf::Mouse::Left) {
                    sf::Vector2i mousePos = sf::Mouse::getPosition(mainWindow);
                    if (button.getGlobalBounds().contains(mousePos.x, mousePos.y)) {
                        threads.emplace_back(createNewWindow);
                    }
                }
            }
        }

        mainWindow.clear();
        mainWindow.draw(button);
        mainWindow.draw(buttonText);
        mainWindow.display();

        // Clean up finished threads
        threads.erase(std::remove_if(threads.begin(), threads.end(),
            [](std::thread& t) { return t.joinable(); }), threads.end());
    }

    // Join all threads before exiting
    for (auto& thread : threads) {
        if (thread.joinable()) {
            thread.join();
        }
    }

    return 0;
}
