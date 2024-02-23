#include <iostream>
#include <string>
#include <ginac/ginac.h>

int main() {
    std::cout << "Enter an expression: ";
    std::string input;
    std::getline(std::cin, input);

    GiNaC::symbol x, y; // Define symbols x and y
    GiNaC::symtab table;
    table["x"] = x;
    table["y"] = y;
    GiNaC::parser reader(table);

    try {
        GiNaC::ex e = reader(input);
        std::cout << "Expression parsed successfully." << std::endl;

        // Canonicalize the parsed expression
        GiNaC::ex canonical_expression = GiNaC::canonicalize(e);
        // Simplify the canonicalized expression
        GiNaC::ex simplified_expression = GiNaC::factor(canonical_expression);
        std::cout << "Parsed expression (simplified): " << simplified_expression << std::endl;
    } catch (std::exception &p) {
        std::cerr << "Error: " << p.what() << std::endl;
    }

    return 0;
}