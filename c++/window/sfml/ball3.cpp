#include <SFML/Graphics.hpp>
#include <eigen3/Eigen/Dense>
#include <vector>
#include <cmath>
#include <thread>
#include <chrono>

constexpr size_t HEIGHT = 400;
constexpr size_t WIDTH = 600;

sf::RenderWindow window(sf::VideoMode(WIDTH, HEIGHT), "");

template<typename T>
class Ball {
public:
	sf::CircleShape Shape;
	Eigen::Vector2<T> position;
	Eigen::Vector2<T> velocity;
	
	const T radius;
	
	Ball(const T posX, const T posY, const T radius, const T velX, const T velY, const sf::Color color = sf::Color::Black) : position(posX, posY), Shape(radius), velocity(velX, velY), radius(radius) {
		Shape.setPosition(posX, posY);
		Shape.setFillColor(color);
	}
	
	void setPosition(const Eigen::Vector2<T>& vec) noexcept {
		Shape.setPosition(vec[0], vec[1]);
		position = vec;
	}
	
	inline void updateShape() noexcept {
		Shape.setPosition(position[0], position[1]);
	}
	
	inline void nextPos() noexcept {
		position += velocity;
	}
	
};

std::vector<Ball<double>> balls;

template<typename T>
void wallCollision(Ball<T>& ball) {
	if (0 >= ball.position[0] || WIDTH - ball.radius * 2 <= ball.position[0]) {
		ball.velocity[0] *= -1;
	} if (0 >= ball.position[1] || HEIGHT - ball.radius * 2 <= ball.position[1]) {
		ball.velocity[1] *= -1;
	}
}

template<typename T, typename U = float>
void ballCollision(Ball<T>& ball0, Ball<T>& ball1) {
	const Eigen::Vector2<U> distanceVec = ball1.position.template cast<U>() - ball0.position.template cast<U>();
	const U distance = distanceVec.squaredNorm();
	
	if (distance <= (ball0.radius + ball1.radius) * (ball0.radius + ball1.radius)) {
		const Eigen::Vector2<U> v0 = ball0.velocity.template cast<U>();
		const Eigen::Vector2<U> v1 = ball1.velocity.template cast<U>();
		
		const U mass0 = ball0.radius;
		const U mass1 = ball1.radius;
		
		const Eigen::Vector2<U> dNormal = distanceVec / std::sqrt(distance);
		
		const U v0Normal = v0.dot(dNormal);
		const U v1Normal = v1.dot(dNormal);
		
		const U v0PrimeNormal = ((mass0 - mass1) * v0Normal + 2*mass1*v1Normal) / (mass0 + mass1);
		const U v1PrimeNormal = ((mass1 - mass0) * v1Normal + 2*mass0*v0Normal) / (mass0 + mass1);
		
		const Eigen::Vector2<U> v0PrimeTangent = v0 - v0Normal * dNormal;
		const Eigen::Vector2<U> v1PrimeTangent = v1 - v1Normal * dNormal;
		
		const Eigen::Vector2<U> v0Final = v0PrimeNormal * dNormal + v0PrimeTangent;
		const Eigen::Vector2<U> v1Final = v1PrimeNormal * dNormal + v1PrimeTangent;
		
		ball0.velocity = v0Final.template cast<T>();
		ball1.velocity = v1Final.template cast<T>();
	}
}

void renderScreen() {
	while (window.isOpen()) {
		for (Ball<double>& ball : balls) {
			wallCollision<double>(ball);
			
			ball.nextPos();
			ball.updateShape();
		}
		
		for (size_t i = 0; i < balls.size() - 1; ++i) {
			for (size_t j = i + 1; j < balls.size(); ++j) {
				ballCollision<double, double>(balls[i], balls[j]);
			}
		}
		
		std::this_thread::sleep_for(std::chrono::milliseconds(10));
	}
}

int main() {
	window.setPosition(sf::Vector2i(0, 0));
	//window.setFramerateLimit(60);
	
	balls.emplace_back(150, 80, 20, -1, -1);
	balls.emplace_back(80, 150, 20, 1, -1);
	balls.emplace_back(150, 150, 20, -1, 1);
	
	std::thread render(renderScreen);
	
	while (window.isOpen()) {
		sf::Event event;
		while (window.pollEvent(event)) {
			if (event.type == sf::Event::Closed)
				window.close();
		}
		
		window.clear(sf::Color::White);
		
		for (const Ball<double>& ball : balls) {
			window.draw(ball.Shape);
		}
		
		window.display();
	}
	
	render.join();
}