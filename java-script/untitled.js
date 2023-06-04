let random = (x) => {
	x ^= x << 13;
	x ^= x >> 17;
	x ^= x << 5;
	return ((x < 0 ? ~x + 1 : x) % 100) / 100;
};
let z = 546;
let a = [5, 3, 3, 5, 7, 8, 5, 4];
a.sort((x) => {
	z ^= z << 43;
	return random(z) - 0.5;
});
console.log(a);