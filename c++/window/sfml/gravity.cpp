#include <SFML/Graphics.hpp>

constexpr size_t HEIGHT = 400;
constexpr size_t WIDTH = 600;

sf::RenderWindow window(sf::VideoMode(WIDTH, HEIGHT), "");

int main() {
	window.setPosition(sf::Vector2i(0, 0));
	window.setFramerateLimit(60);

	// Create a circle
	sf::CircleShape circle(40);  // Circle with radius 50
	circle.setFillColor(sf::Color::Black);
	circle.setPosition(350, 275);  // Initial position

	bool isDragging = false;		  // Whether the circle is being dragged
	sf::Vector2f offset;			  // Offset between the mouse and circle's position

	while (window.isOpen()) {
		sf::Event event;
		while (window.pollEvent(event)) {
			if (event.type == sf::Event::Closed) {
				window.close();
			}

			// Check for mouse button press
			if (event.type == sf::Event::MouseButtonPressed && event.mouseButton.button == sf::Mouse::Left) {
				// Check if mouse is inside the circle
				if (circle.getGlobalBounds().contains(window.mapPixelToCoords(sf::Mouse::getPosition(window)))) {
					isDragging = true;
					// Calculate offset
					offset = circle.getPosition() - window.mapPixelToCoords(sf::Mouse::getPosition(window));
				}
			}

			// Check for mouse button release
			if (event.type == sf::Event::MouseButtonReleased && event.mouseButton.button == sf::Mouse::Left) {
				isDragging = false;
			}
		}

		// Handle dragging
		if (isDragging) {
			circle.setPosition(window.mapPixelToCoords(sf::Mouse::getPosition(window)) + offset);
		}

		// Clear window and draw
		window.clear(sf::Color::White);
		window.draw(circle);
		window.display();
	}

	return 0;
}