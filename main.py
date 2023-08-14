from antlr4 import *
from ArithmeticLexer import ArithmeticLexer
from ArithmeticParser import ArithmeticParser

class ArithmeticVisitor(ParseTreeVisitor):

    def __init__(self, variaveis) -> None:
        super().__init__()
        self.variaveis = variaveis

    def visitExpr(self, ctx):
        result = self.visitTerm(ctx.term(0))
        for i in range(1, len(ctx.term())):
            if ctx.getChild(i*2-1).getText() == '+':
                result += self.visitTerm(ctx.term(i))
            else:
                result -= self.visitTerm(ctx.term(i))
        return result

    def visitTerm(self, ctx):
        result = self.visitFactor(ctx.factor(0))
        for i in range(1, len(ctx.factor())):
            if ctx.getChild(i*2-1).getText() == '*':
                result *= self.visitFactor(ctx.factor(i))
            else:
                result /= self.visitFactor(ctx.factor(i))
        return result
    
    def visitAssignment(self, ctx):
        result = self.visitExpr(ctx.expr()) 
        self.variaveis[ctx.VAR().getText()] = result

        return result

    def visitFactor(self, ctx):
        if ctx.INT():
            return int(ctx.INT().getText())
        
        elif ctx.VAR():
            return int(self.variaveis[ctx.VAR().getText()])
        else:
            return self.visitExpr(ctx.expr())
        
    def visitProgram(self, ctx):
    
        return self.visitStatement(ctx.statement()), self.variaveis

    def visitStatement(self, ctx):
        #Prmeiros temos que definir se a entrada é uma exp ou um assigment
        for x in ctx:  
            if x.assignment():  
                result = self.visitAssignment(x.assignment())

            else:
                result = self.visitExpr(x.expr()) 

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
        result, variaveis = visitor.visitProgram(tree)
        print("Resultado:", result)
        expression = input("Digite uma expressão aritmética: ")

if __name__ == '__main__':
    main()