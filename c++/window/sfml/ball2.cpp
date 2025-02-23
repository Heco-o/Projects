#include <SFML/Graphics.hpp>
#include <vector>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <thread>
#include <mutex>

// Constants
const int WIDTH = 800;	// Width of the rectangular area
const int HEIGHT = 600;   // Height of the rectangular area
const float BALL_RADIUS = 40.0f;
const float TIME_STEP = 0.01f;  // Time step for the simulation in seconds

// Ball class definition
class Ball {
public:
	Ball(float x, float y, float vx, float vy, float radius, sf::Color color)
		: x(x), y(y), vx(vx), vy(vy), radius(radius) {
		shape.setRadius(radius);
		shape.setFillColor(color);
		shape.setOrigin(radius, radius);
		shape.setPosition(x, y);
	}

	void updatePosition() {
		x += vx * TIME_STEP;
		y += vy * TIME_STEP;
		shape.setPosition(x, y);
	}

	void checkWallCollision() {
		// Check collision with the left and right walls
		if (x - radius < 0 || x + radius > WIDTH) {
			vx = -vx;
			x = std::max(radius, std::min(x, WIDTH - radius));
		}

		// Check collision with the top and bottom walls
		if (y - radius < 0 || y + radius > HEIGHT) {
			vy = -vy;
			y = std::max(radius, std::min(y, HEIGHT - radius));
		}
	}

	void checkBallCollision(Ball& other) {
		// Calculate the distance between the two balls
		float dx = other.x - x;
		float dy = other.y - y;
		float distanceSquared = dx * dx + dy * dy;

		if (distanceSquared < (other.radius + radius) * (other.radius + radius)) {  // Compare squared distances
			float distance = std::sqrt(distanceSquared);
			float overlap = other.radius + radius - distance;

			if (distance == 0) {  // Avoid division by zero
				return;
			}

			// Calculate unit normal and tangential vectors
			float nx = dx / distance;
			float ny = dy / distance;
			float tx = -ny;
			float ty = nx;

			// Calculate relative velocity components along normal and tangential vectors
			float v1n = vx * nx + vy * ny;
			float v1t = vx * tx + vy * ty;
			float v2n = other.vx * nx + other.vy * ny;
			float v2t = other.vx * tx + other.vy * ty;

			// Calculate new normal velocities using one-dimensional elastic collision formula
			float m1 = radius;  // Assuming equal mass balls
			float m2 = other.radius;
			float v1n_final = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2);
			float v2n_final = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2);

			// Convert normal velocities back to original coordinate system
			vx = v1n_final * nx + v1t * tx;
			vy = v1n_final * ny + v1t * ty;
			other.vx = v2n_final * nx + v2t * tx;
			other.vy = v2n_final * ny + v2t * ty;

			// Move the balls apart to prevent overlap
			x -= overlap * nx / 2;
			y -= overlap * ny / 2;
			other.x += overlap * nx / 2;
			other.y += overlap * ny / 2;
		}
	}

	void draw(sf::RenderWindow& window) {
		window.draw(shape);
	}

private:
	float x, y;
	float vx, vy;
	float radius;
	sf::CircleShape shape;
};

std::mutex ballsMutex;
std::vector<Ball> balls;

void simulate() {
	while (true) {
		std::lock_guard<std::mutex> lock(ballsMutex);
		for (auto& ball : balls) {
			ball.updatePosition();
			ball.checkWallCollision();
		}

		// Check collisions between all pairs of balls
		for (std::size_t i = 0; i < balls.size(); ++i) {
			for (std::size_t j = i + 1; j < balls.size(); ++j) {
				balls[i].checkBallCollision(balls[j]);
			}
		}
		std::this_thread::sleep_for(std::chrono::milliseconds(static_cast<int>(TIME_STEP * 1000)));
	}
}

int main() {
	std::srand(static_cast<unsigned int>(std::time(nullptr)));

	sf::RenderWindow window(sf::VideoMode(WIDTH, HEIGHT), "Bouncing Balls Simulation");

	// Initialize balls with random positions and velocities
	sf::Color colors[] = { sf::Color::Blue, sf::Color::Red, sf::Color::Green, sf::Color::Yellow, sf::Color::Black, sf::Color::Magenta };
	for (int i = 0; i < 6; ++i) {
		balls.emplace_back(
			static_cast<float>(std::rand()) / static_cast<float>(RAND_MAX) * (WIDTH - 2 * BALL_RADIUS) + BALL_RADIUS,
			static_cast<float>(std::rand()) / static_cast<float>(RAND_MAX) * (HEIGHT - 2 * BALL_RADIUS) + BALL_RADIUS,
			static_cast<float>(std::rand()) / static_cast<float>(RAND_MAX) * 400 - 200,
			static_cast<float>(std::rand()) / static_cast<float>(RAND_MAX) * 400 - 200,
			BALL_RADIUS,
			colors[i]
		);
	}

	// Start the simulation in a separate thread
	std::thread simulationThread(simulate);

	while (window.isOpen()) {
		sf::Event event;
		while (window.pollEvent(event)) {
			if (event.type == sf::Event::Closed)
				window.close();
		}

		window.clear();
		{
			std::lock_guard<std::mutex> lock(ballsMutex);
			for (auto& ball : balls) {
				ball.draw(window);
			}
		}
		window.display();
	}

	simulationThread.join();
	return 0;
}