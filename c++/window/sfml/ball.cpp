#include <SFML/Graphics.hpp>
#include <iostream>

const int ballSize = 20;
const int screenWidth = 800;
const int screenHeight = 600;
const int initialX = screenWidth / 2;
const int initialY = screenHeight / 2;

// Create SFML window
sf::RenderWindow window(sf::VideoMode(screenWidth, screenHeight), "Bouncing Ball");

int main() {
	window.setVerticalSyncEnabled(true);

	// Create SFML circle shape for the ball
	sf::CircleShape ball(ballSize);
	ball.setFillColor(sf::Color::Black);
	ball.setPosition(initialX, initialY);

	// Set initial direction of the ball
	int xDirection = 1;
	int yDirection = 1;
	while (window.isOpen()) {
		sf::Event event;
		while (window.pollEvent(event)) {
			if (event.type == sf::Event::Closed)
				window.close();
		}

		// Update ball position
		sf::Vector2f position = ball.getPosition();
		position.x += xDirection;
		position.y += yDirection;
		ball.setPosition(position);

		// Bounce off the walls
		if (position.x <= 0 || position.x >= (screenWidth - ballSize))
			xDirection *= -1;

		if (position.y <= 0 || position.y >= (screenHeight - ballSize))
			yDirection *= -1;

		// Clear the window
		window.clear(sf::Color::White);

		// Draw the ball
		window.draw(ball);

		// Display the window
		window.display();
	}

	return 0;
}
