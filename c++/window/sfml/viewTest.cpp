#include <SFML/Graphics.hpp>

int main() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "View Example");

    // Create a view centered at (400, 300) with a size of (800, 600)
    sf::View view(sf::Vector2f(400, 300), sf::Vector2f(800, 600));

    // Attach the view to the window
    window.setView(view);

    // Create a simple rectangle to demonstrate the view
    sf::RectangleShape rectangle(sf::Vector2f(1600, 1200)); // Big rectangle
    rectangle.setFillColor(sf::Color::Green);
    rectangle.setPosition(0, 0);

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
            }

            // Pan the view with arrow keys
            if (sf::Keyboard::isKeyPressed(sf::Keyboard::Left)) {
                view.move(-5, 0); // Move left
            }
            if (sf::Keyboard::isKeyPressed(sf::Keyboard::Right)) {
                view.move(5, 0); // Move right
            }
            if (sf::Keyboard::isKeyPressed(sf::Keyboard::Up)) {
                view.move(0, -5); // Move up
            }
            if (sf::Keyboard::isKeyPressed(sf::Keyboard::Down)) {
                view.move(0, 5); // Move down
            }

            // Zoom the view with +/- keys
            if (sf::Keyboard::isKeyPressed(sf::Keyboard::Add)) {
                view.zoom(0.95f); // Zoom in (smaller factor zooms in)
            }
            if (sf::Keyboard::isKeyPressed(sf::Keyboard::Subtract)) {
                view.zoom(1.05f); // Zoom out
            }
        }

        // Apply the updated view to the window
        window.setView(view);

        // Draw everything
        window.clear(sf::Color::White);
        window.draw(rectangle);
        window.display();
    }

    return 0;
}
