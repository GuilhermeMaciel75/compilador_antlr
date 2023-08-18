from antlr4 import *
from ArithmeticLexer import ArithmeticLexer
from ArithmeticParser import ArithmeticParser

class ArithmeticVisitor(ParseTreeVisitor):

    def __init__(self, variaveis) -> None:
        super().__init__()
        self.variaveis = variaveis

    def visit(self, ctx):
        if isinstance(ctx, ArithmeticParser.ExprContext):
            return self.visitExpr(ctx)
        
        elif isinstance(ctx, ArithmeticParser.TermContext):
            return self.visitTerm(ctx)
        
        elif isinstance(ctx, ArithmeticParser.FactorContext):
            return self.visitFactor(ctx)
        
        elif isinstance(ctx, ArithmeticParser.AssignmentContext):
            return self.visitAssignment(ctx)
        
        elif isinstance(ctx, ArithmeticParser.ProgramContext):
            return self.visitProgram(ctx)
        
        elif isinstance(ctx, ArithmeticParser.StatementContext):
            return self.visitStatement(ctx)

    def visitExpr(self, ctx):
        result = self.visit(ctx.term(0))
        for i in range(1, len(ctx.term())):
            if ctx.getChild(i * 2 - 1).getText() == '+':
                result += self.visit(ctx.term(i))
            else:
                result -= self.visit(ctx.term(i))
        return result

    def visitTerm(self, ctx):
        result = self.visit(ctx.factor(0))
        for i in range(1, len(ctx.factor())):
            if ctx.getChild(i * 2 - 1).getText() == '*':
                result *= self.visit(ctx.factor(i))
            else:
                result /= self.visit(ctx.factor(i))
        return result

    def visitAssignment(self, ctx):
        result = self.visit(ctx.expr()) 
        self.variaveis[ctx.VAR().getText()] = result

        return result

    def visitFactor(self, ctx):
        if ctx.INT():
            return int(ctx.INT().getText())
        
        elif ctx.VAR():
            return int(self.variaveis[ctx.VAR().getText()])
        else:
            return self.visit(ctx.expr())
        
    def visitProgram(self, ctx):
        for sta in ctx.statement():  
            return self.visit(sta), self.variaveis

    def visitStatement(self, ctx):
        #Prmeiros temos que definir se a entrada é uma exp ou um assigment
        if ctx.assignment():  
            result = self.visit(ctx.assignment())

        else:
            result = self.visit(ctx.expr()) 

        return result
 

def main():
    variaveis = {}
    print("Digite \"fim\" para sair")
    expression = input("Digite uma expressão aritmética: ")

    while expression.lower() != 'fim':
        lexer = ArithmeticLexer(InputStream(expression))
        stream = CommonTokenStream(lexer)
        parser = ArithmeticParser(stream)
        tree = parser.program()
        visitor = ArithmeticVisitor(variaveis)
        result, variaveis = visitor.visit(tree)
        print("Resultado:", result)
        expression = input("Digite uma expressão aritmética: ")

if __name__ == '__main__':
    main()