# ParsarAssignement

Grammar of the language:

program ::= statement*
statement ::= assign_stmt | if_stmt | while_stmt | expr_stmt | function_call
assign_stmt ::= IDENTIFIER '=' expression
if_stmt ::= 'if' boolean_expression ':' block ('else' ':' block)?
while_stmt ::= 'while' boolean_expression ':' block
block ::= statement*
expr_stmt ::= expression
function_call ::= IDENTIFIER '(' arg_list? ')'
arg_list ::= expression (',' expression)*
boolean_expression ::= term (( '==' | '!=' | '>' | '<' ) term)*
expression ::= term (( '+' | '-' ) term)*
term ::= factor (( '*' | '/' ) factor)*
factor ::= NUMBER | IDENTIFIER | '(' expression ')'
IDENTIFIER ::= [a-zA-Z_][a-zA-Z0-9_]*
NUMBER ::= [0-9]+


Example:

Let’s take the following program and understand the derivation:
x = 10
if x > 10:
foo(x + 20)


This program has two statements:

1. x = 10
2. if x > 10: foo(x + 20)

The first statement is an assignment statement : x = 10
statement ::= assign_stmt | if_stmt | while_stmt | expr_stmt | function_call
Derive statement (x = 10):
statement ::= assign_stmt
assign_stmt ::= IDENTIFIER '=' expression
Derive expression:
expression ::= term (( '+' | '-' ) term)*
term ::= factor (( '*' | '/' ) factor)*
factor ::= NUMBER | IDENTIFIER | '(' expression ')'
Derive number:
factor ::= NUMBER
NUMBER ::= 10
Full derivation of the statement : x = 10
assign_stmt ::= IDENTIFIER '=' expression
IDENTIFIER ::= x
expression ::= term
term ::= factor
factor ::= NUMBER
NUMBER ::= 10
The second statement is ( if x > 10: foo(x + 20))
statement ::= if_stmt
if_stmt ::= 'if' boolean_expression ':' block ('else' ':' block)?
First derive boolean expression:
boolean_expression ::= term (( '==' | '!=' | '>' | '<' ) term)*
Derivation for boolean expression:
boolean_expression ::= term '>' term
term ::= factor
factor ::= IDENTIFIER
IDENTIFIER ::= x
term ::= factor
factor ::= NUMBER
NUMBER ::= 10
Next we derive block part of the if statement:
block ::= statement*
statement ::= function_call
function_call ::= IDENTIFIER '(' arg_list? ')'
arg_list ::= expression (',' expression)*
expression ::= term (( '+' | '-' ) term)*
term ::= factor
factor ::= IDENTIFIER
IDENTIFIER ::= x
term ::= factor
factor ::= NUMBER
NUMBER ::= 20
Entire derivation of the second statement is:
statement ::= if_stmt
if_stmt ::= 'if' boolean_expression ':' block
boolean_expression ::= term '>' term
term ::= factor
factor ::= IDENTIFIER
IDENTIFIER ::= x
term ::= factor
factor ::= NUMBER
NUMBER ::= 10
block ::= statement
statement ::= function_call
function_call ::= IDENTIFIER '(' arg_list ')'
IDENTIFIER ::= foo
arg_list ::= expression
expression ::= term '+' term
term ::= factor
factor ::= IDENTIFIER
IDENTIFIER ::= x
term ::= factor
factor ::= NUMBER
NUMBER ::= 20
Test case and their AST representations:
We have provide few representations of AST for some the test cases in the project.
Test case 1:
x = 5
y = y + x
AST representation:
[Assignment(
('IDENTIFIER', 'x'),
('NUMBER', 5)
), Assignment(
('IDENTIFIER', 'y'),
BinaryOperation(
('IDENTIFIER', 'y'),
('PLUS', '+'),
('IDENTIFIER', 'x')
)
)]


Project Sections:

1. Lexer:

a lexer to tokenize input code into meaningful tokens (e.g., keywords,
operators, identifiers, numbers). Handles basic tokens like if, else, while, +, -, *, /, =, !=, ==, <, >, (, ), :, etc.


2. Parser:
a parser that converts a token stream into an Abstract Syntax Tree (AST). parsing logic for different constructs like assignment statements (x =
expression), binary operations (expression1 + expression2), boolean expressions (x == y), if-else statements, while loops, and function calls.

