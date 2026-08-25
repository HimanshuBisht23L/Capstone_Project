import ast

class SecurityError(Exception):
    """Raised when dangerous code constructs are detected in static AST analysis."""
    pass

class SecurityASTVisitor(ast.NodeVisitor):
    BLOCKED_MODULES = {
        "os", "sys", "subprocess", "shutil", "socket", "urllib",
        "requests", "httpx", "importlib", "ctypes", "multiprocessing", "threading"
    }
    
    BLOCKED_BUILTINS = {
        "eval", "exec", "open", "__import__", "globals", "locals",
        "getattr", "setattr", "delattr", "compile", "breakpoint"
    }

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            module_name = alias.name.split(".")[0]
            if module_name in self.BLOCKED_MODULES:
                raise SecurityError(f"Security Violation: Import of module '{alias.name}' is strictly forbidden.")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            module_name = node.module.split(".")[0]
            if module_name in self.BLOCKED_MODULES:
                raise SecurityError(f"Security Violation: Import from module '{node.module}' is strictly forbidden.")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in self.BLOCKED_BUILTINS:
                raise SecurityError(f"Security Violation: Execution of builtin function '{func_name}' is strictly forbidden.")
        self.generic_visit(node)


def verify_code_security(python_code: str) -> bool:
    """
    Parses Python code into an AST and verifies it against static security rules.
    Returns True if code is safe; raises SecurityError if code contains violations.
    """
    try:
        tree = ast.parse(python_code)
    except SyntaxError as e:
        raise SecurityError(f"AST Parsing Syntax Error: {e}")

    visitor = SecurityASTVisitor()
    visitor.visit(tree)
    return True
