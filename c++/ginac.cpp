#include <iostream>
#include <ginac/ginac.h>

int main() {
    GiNaC::symbol x, y;
    GiNaC::symtab table;
    table["x"] = x;
    table["y"] = y;
    GiNaC::parser reader(table);

    std::string eqn1_str, eqn2_str;

    std::cout << "Enter the first equation in the form 'expression == expression': ";
    std::getline(std::cin, eqn1_str);
    GiNaC::ex eqn1;
    try {
        eqn1 = reader(eqn1_str);
        std::cout << "Parsed expression: " << eqn1 << std::endl;
    } catch (std::exception &p) {
        std::cerr << p.what() << std::endl;
        return 1;
    }

    std::cout << "Enter the second equation in the form 'expression == expression': ";
    std::getline(std::cin, eqn2_str);
    GiNaC::ex eqn2;
    try {
        eqn2 = reader(eqn2_str);
        std::cout << "Parsed expression: " << eqn2 << std::endl;
    } catch (std::exception &p) {
        std::cerr << p.what() << std::endl;
        return 1;
    }

    // List of equations
    GiNaC::lst eqns = {eqn1 == 0, eqn2 == 0}; // Convert to equation form

    // List of variables
    GiNaC::lst vars = {x, y};

    // Solve equations
    GiNaC::ex e = GiNaC::lsolve(eqns, vars);

    // Print solutions
    std::cout << "Solutions for x and y:" << std::endl;
    std::cout << e << std::endl;

    return 0;
}