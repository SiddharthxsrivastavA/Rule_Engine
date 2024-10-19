# Rule_Engine

Overview
This project implements a rule engine using an Abstract Syntax Tree (AST) to dynamically create, combine, and evaluate conditional rules. It supports rules with operators like AND and OR, which are applied to conditions such as "age > 30" or "department = 'Sales'." The rule engine is designed to evaluate user eligibility based on their attributes, and it integrates with PostgreSQL to store rules and metadata.

Features
Create Rules: Dynamically create rules from string inputs.
Combine Rules: Combine multiple rules into one AST.
Evaluate Rules: Evaluate user data against the combined rules to determine eligibility.
Database Integration: Store rules and metadata using PostgreSQL.
Relational Design: Self-referencing table for AST nodes to represent rules.

Testing:

Sample rules:
rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
rule2 = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
Sample user data:
user_data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
To test the evaluation:
python main.py


Non-Functional Requirements

Security:
PostgreSQL connection uses SSL to secure communication (configure in config.py if needed).
Input validation ensures rule strings and user data are well-formed.
Performance:
AST optimizes the evaluation process by reducing redundant operations.
Efficient querying of rules from PostgreSQL using indexed fields.




