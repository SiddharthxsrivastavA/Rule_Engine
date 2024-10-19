class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # Can be "operator" (AND, OR) or "operand" (condition)
        self.left = left  # Left child (another Node)
        self.right = right  # Right child (another Node)
        self.value = value  # The condition value for operands (e.g., age > 30)

    def __repr__(self):
        return f"Node({self.type}, {self.left}, {self.right}, {self.value})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type=None):
        token = self.current_token()
        print(f"Consuming token: {token}, Expected: {expected_type}")  # Debugging line
        if expected_type and token[0] != expected_type:
            raise ValueError(f'Expected token type {expected_type}, got {token[0]} at position {self.pos}')
        self.pos += 1
        return token

    def parse_expression(self):
        node = self.parse_term()
        while self.current_token() and self.current_token()[0] == 'OR':
            self.consume('OR')
            right = self.parse_term()
            node = Node("operator", left=node, right=right, value="OR")
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token() and self.current_token()[0] == 'AND':
            self.consume('AND')
            right = self.parse_factor()
            node = Node("operator", left=node, right=right, value="AND")
        return node

    def parse_factor(self):
        token = self.current_token()
        if token[0] == 'LPAREN':
            self.consume('LPAREN')
            node = self.parse_expression()
            self.consume('RPAREN')
            return node
        elif token[0] == 'IDENT':
            condition = self.parse_condition()
            return Node("operand", value=condition)
        else:
            raise ValueError(f"Unexpected token {token[0]} at position {self.pos}")

    def parse_condition(self):
        attribute = self.consume('IDENT')[1]
        operator = self.consume('OPERATOR')[1]
        value = self.consume('IDENT')[1]
        return f"{attribute} {operator} {value}"


def tokenize(rule_string):
    import re
    token_specification = [
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('AND', r'AND'),
        ('OR', r'OR'),
        ('OPERATOR', r'[><=]'),
        ('IDENT', r"[a-zA-Z0-9_']+"),
        ('SKIP', r'[ \t\n]+'),
    ]
    token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
    tokens = []
    for match in re.finditer(token_regex, rule_string):
        kind = match.lastgroup
        value = match.group()
        if kind != 'SKIP':
            tokens.append((kind, value))
    return tokens


def create_rule(rule_string):
    tokens = tokenize(rule_string)
    print(f"Tokenized rule: {tokens}")  # Debugging print
    parser = Parser(tokens)
    ast = parser.parse_expression()
    return ast


def combine_rules(rule_asts):
    if not rule_asts:
        return None

    root = rule_asts[0]
    for rule_ast in rule_asts[1:]:
        print(f"Combining rule: {rule_ast}")  # Debug print
        root = Node("operator", left=root, right=rule_ast, value="OR")
    return root


def evaluate_rule(ast, user_data):
    print(f"\nEvaluating node: {ast}")  # Debug print

    if ast is None:
        print("Error: Node is None")
        return False

    if ast.type == "operand":
        result = evaluate_condition(ast.value, user_data)
        print(f"Evaluating condition: {ast.value} -> {result}")  # Show condition evaluation
        return result

    if ast.type == "operator":
        left_result = evaluate_rule(ast.left, user_data)
        right_result = evaluate_rule(ast.right, user_data)

        result = left_result and right_result if ast.value == "AND" else left_result or right_result
        print(f"Evaluating operator: {ast.value} -> {left_result} {ast.value} {right_result} = {result}")  # Show operator evaluation
        return result

    raise ValueError(f"Unsupported node type: {ast.type}")


def evaluate_condition(condition, user_data):
    attribute, operator, value = condition.split()
    value = int(value) if value.isdigit() else value.strip("'")

    # Fetch the attribute value from user_data
    attribute_value = user_data.get(attribute)
    if attribute_value is None:
        print(f"Error: {attribute} not found in user data.")
        return False

    # Handle various comparison operations
    if operator == ">":
        return attribute_value > value
    elif operator == "<":
        return attribute_value < value
    elif operator == "=":
        return attribute_value == value

    raise ValueError(f"Unsupported operator: {operator}")


# Test the rule engine
rule1_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
rule2_string = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"

# Create ASTs for both rules
rule1_ast = create_rule(rule1_string)
rule2_ast = create_rule(rule2_string)

# Combine the ASTs into one (this will create combined_ast)
combined_ast = combine_rules([rule1_ast, rule2_ast])

# Print the combined AST to see the structure
print("\nCombined AST:", combined_ast)

# Test the evaluation function with a sample user data
user_data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
result = evaluate_rule(combined_ast, user_data)

print("\nFinal Evaluation result:", result)  # Should print True if the user matches the rule



'''


DataBase Choice:

Relational Database (PostgreSQL/MySQL): Since the AST structure involves parent-child relationships (nodes), a relational database with self-referencing tables (for AST nodes) can be used. Additionally, a relational database allows us to define metadata schemas and relationships between rules and users.


Reasons for choosing a relational database:

AST nodes can be modeled using a self-referencing table.
It supports ACID transactions, ensuring the correctness of rule changes.
SQL queries can be optimized for checking, modifying, and retrieving specific parts of the AST efficiently.
Rules and metadata (like user attributes) can be stored and queried efficiently using a relational structure.



Schema Design:

-- Insert rule metadata
INSERT INTO rules (rule_name, description, created_at) 
VALUES ('Rule 1', 'Age and department-based rule with salary and experience check', NOW());

-- Insert AST nodes for Rule 1
INSERT INTO ast_nodes (rule_id, type, operator, value, left_node_id, right_node_id, created_at)
VALUES 
(1, 'operator', 'AND', NULL, 2, 3, NOW()),  -- Root AND node
(1, 'operator', 'OR', NULL, 4, 5, NOW()),  -- Left OR node
(1, 'operand', NULL, 'age > 30 AND department = Sales', NULL, NULL, NOW()),  -- Left child operand
(1, 'operand', NULL, 'age < 25 AND department = Marketing', NULL, NULL, NOW()),  -- Right child operand
(1, 'operator', 'OR', NULL, 6, 7, NOW()),  -- Right OR node
(1, 'operand', NULL, 'salary > 50000', NULL, NULL, NOW()),  -- Left child operand
(1, 'operand', NULL, 'experience > 5', NULL, NULL, NOW());  -- Right child operand


'''