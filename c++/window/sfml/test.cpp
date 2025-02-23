#include <SFML/Graphics.hpp>

int main() {
    // Create a window
    sf::RenderWindow window(sf::VideoMode(800, 600), "SFML Circle");

    // Main loop
    while (window.isOpen()) {
        // Handle events
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        // Clear the window
        window.clear(sf::Color::White);

        // Draw a circle
        sf::CircleShape circle(100);
        circle.setFillColor(sf::Color::Blue);
        circle.setPosition(350, 250);
        window.draw(circle);

        // Display the window
        window.display();
    }

    return 0;
}
