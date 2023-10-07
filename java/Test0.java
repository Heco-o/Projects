package symjava.examples;

import static symjava.symbolic.Symbol.*;
import symjava.bytecode.BytecodeFunc;
import symjava.symbolic.*;

public class Example1 {

    public static void main(String[] args) {
        Expr expr = x.add(y.mul(z)); // Use add() and mul() methods for addition and multiplication
        System.out.println(expr); // x + y*z

        Expr expr2 = expr.subs(x, y.pow(2)); // Use pow() method for exponentiation
        System.out.println(expr2); // y^2 + y*z
        System.out.println(expr2.diff(y)); // 2*y + z

        Func f = new Func("f1", expr2.diff(y));
        System.out.println(f); // 2*y + z

        BytecodeFunc func = f.toBytecodeFunc();
        System.out.println(func.apply(1, 2)); // 4.0
    }
}