import ast, multiprocessing as mp, sys, CommentReader, astor, random

class NewVisitor(ast.NodeVisitor):
    numberLoopDictionary = {}
    def visit_For(self, node):
        self.numberLoopDictionary[str(node.lineno)] = node
        self.generic_visit(node)


def getNodeToReplace(node):
    if isinstance(node, ast.For):
        astobject = ast.FunctionDef
        return astobject


def instrumentCode(tree, parallelLineNumbers = []):
    #print(parallelLineNumbers)
    print('inputCode:')
    print(astor.to_source(tree))
    print('-------------')
    visitor = NewVisitor()
    visitor.visit(tree)
    numberLoopDictionary = visitor.numberLoopDictionary
    #print(numberLoopDictionary)
    statements = []
    for statement in tree.body:
        if isinstance(statement, ast.FunctionDef) and (statement.lineno - 1) in parallelLineNumbers:
            parallelLineNumbers.remove(statement.lineno - 1)
            stmts = []
            #print('statement =', statement)
            for stmt in statement.body:
                if isinstance(stmt, ast.For):
                    newstmt = instrumentFunctionBody(stmt)
                    stmts += newstmt
                else:
                    stmts.append(stmt)
            statement.body = stmts
            #print('next',statement)
        statements.append(statement)
    statements2 = []
    for statement in statements:
        if isinstance(statement, ast.For) and (statement.lineno - 1) in parallelLineNumbers:
            parallelLineNumbers.remove(statement.lineno - 1)
            statement = instrumentBody(statement)
        statements2.append(statement)
    tree.body = statements2
    #print('new dump =',ast.dump(tree))
    code = astor.to_source(tree)
    print()
    print('outputCode:')
    print(code)
    return code


def instrumentBody(forLoopStatement):
    #print(ast.dump(forLoopStatement))
    iterator = forLoopStatement.iter
    iterator = eval(astor.to_source(iterator))
    body = []
    bodyStatement = ast.parse("localVariables = locals()")
    body.append(bodyStatement)
    bodyStatement = ast.parse("globalVariables = globals()")
    body.append(bodyStatement)
    for statement in forLoopStatement.body:
        body.append(statement)
    name = 'func' + str(random.randint(1, 1000))
    func = ast.FunctionDef(name = name, args = ast.arguments(args = [ast.arg(arg = forLoopStatement.target.id, annotation = None, vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[])], defaults = [], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None), body=body, decorator_list = [], returns = None)
    statements = []
    statements.append(func)
    statement1 = ast.parse("import multiprocessing as mp")
    statement2 = ast.parse("if __name__ == '__main__': \n\twith mp.Pool() as p: \n\t\t print(p.map(" + name +", "+ str(iterator)+"))")
    statements += [statement1, statement2]
    module = ast.Module(body = statements)
    return module

def instrumentFunctionBody(forLoopStatement):
    iterator = forLoopStatement.iter
    iterator = eval(astor.to_source(iterator))
    body = []
    bodyStatement = ast.parse("localVariables = locals()")
    body.append(bodyStatement)
    bodyStatement = ast.parse("globalVariables = globals()")
    body.append(bodyStatement)
    for statement in forLoopStatement.body:
        body.append(statement)
    name = 'func' + str(random.randint(1, 1000))
    func = ast.FunctionDef(name = name, args = ast.arguments(args = [ast.arg(arg = forLoopStatement.target.id, annotation = None, vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[])], defaults = [], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None), body=body, decorator_list = [], returns = None)
    statements = []
    statements.append(func)
    statement1 = ast.parse("import multiprocessing as mp")
    statement2 = ast.parse("if __name__ == '__main__': \n\twith mp.Pool() as p: \n\t\t print(p.map(" + name +", "+ str(iterator)+"))")
    statements += [statement1, statement2]
    return statements


if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, 'r') as code_file:
        code = code_file.read()
        tree = ast.parse(code)
        linesWithNumber = CommentReader.getLineWithNumber(filename)
        lineNumbersToConsider = CommentReader.getLinesCommentedParallel(linesWithNumber)
        instrumentCode(tree, lineNumbersToConsider)





