import sys
import re


# Class to convert the expression
class Conversion:

    # Constructor to initialize the class variables
    def __init__(self, expression):
        self.expression = expression
        self.top = -1
        # This array is used a stack
        self.array = []
        # Precedence setting
        self.output = []
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    # check if the stack is empty
    def isEmpty(self):
        return True if self.top == -1 else False

    # Return the value of the top of the stack
    def peek(self):
        return self.array[-1]

    # Pop the element from the stack
    def pop(self):
        if not self.isEmpty():
            self.top -= 1
            return self.array.pop()
        else:
            return False

    # Push the element to the stack
    def push(self, op):
        self.top += 1
        self.array.append(op)

    # A utility function to check is the given character
    # is operand
    def isOperand(self, ch):
        return ch.isnumeric()

    # Check if the precedence of operator is strictly
    # less than top of stack or not
    def notGreater(self, i):
        try:
            a = self.precedence[i]
            b = self.precedence[self.peek()]
            return True if a <= b else False
        except KeyError:
            return False

    def infixToPostfix(self):

        # Iterate over the expression for conversion
        for i in self.expression:
            # If the character is an operand,
            # add it to output
            if self.isOperand(i):
                self.output.append(i)

            # If the character is an '(', push it to stack
            elif i == '(':
                self.push(i)

            # If the scanned character is an ')', pop and
            # output from the stack until and '(' is found
            elif i == ')':
                while ((not self.isEmpty()) and
                       self.peek() != '('):
                    self.output.append(self.pop())
                # if expression is invalid
                if not self.isEmpty() and self.peek() != '(':
                    return -1
                else:
                    self.pop()
            # An operator is encountered
            else:
                while not self.isEmpty() and self.notGreater(i):
                    self.output.append(self.pop())
                self.push(i)
        # pop all the operator from the stack
        while not self.isEmpty():
            self.output.append(self.pop())
        return self.output


# Class to convert the expression
class Evaluate:

    # Constructor to initialize the class variables
    def __init__(self, expression):
        self.top = -1
        self.expression = expression
        # This array is used a stack
        self.array = []

    # check if the stack is empty
    def isEmpty(self):
        return True if self.top == -1 else False

    # Return the value of the top of the stack
    def peek(self):
        return self.array[-1]

    # Pop the element from the stack
    def pop(self):
        if not self.isEmpty():
            self.top -= 1
            return self.array.pop()
        else:
            return '$'

    # Push the element to the stack
    def push(self, op):
        self.top += 1
        self.array.append(op)

    # The main function that converts given infix expression
    # to postfix expression
    def evaluatePostfix(self):

        # Iterate over the expression for conversion
        for i in self.expression:

            # If the scanned character is an operand
            # (number here) push it to the stack
            if i.isdigit():
                self.push(i)

            # If the scanned character is an operator,
            # pop two elements from stack and apply it.
            else:
                val1 = self.pop()
                val2 = self.pop()
                self.push(str(eval(val2 + i + val1)))
        return int(float(self.pop()))


class Calculator:
    def __init__(self):
        self.variable_dictionary = {}

    @staticmethod
    def balanced_brackets(inp):
        pairs = {"(": ")"}
        stack = []
        for i in inp:
            if i in "(":
                stack.append(i)
            elif stack and i == pairs[stack[-1]]:
                stack.pop()
            elif not stack and i == ")":
                return False
            else:
                continue
        return len(stack) == 0

    def parse_user_input(self):
        user_input = input()
        # process replacements
        replacements = [('[+]{2,}', '+'), ('[*]{2,}', 'Invalid expression'), ('[/]{2,}', 'Invalid expression'),
                        ('[-]{3,}', '-'), ('[-]{2,}', '+')]
        for old, new in replacements:
            user_input = re.sub(old, new, user_input)
            if 'Invalid expression' in user_input:
                print('Invalid expression')
                user_input = []
                input_type = 'wrong input'
                return user_input, input_type

        # differentiate the input type and parse it accordingly
        if user_input.startswith('/'):
            user_input = user_input.split()
            input_type = 'command'

        elif user_input.strip().isalpha():
            user_input = user_input.strip().split()
            input_type = 'call_variable'

        elif user_input.strip().isnumeric() or user_input.lstrip('-').strip().isnumeric():
            print(user_input.strip())
            user_input = []
            input_type = 'print_digit'

        elif '=' in user_input:
            user_input = [i.strip() for i in user_input.split('=') if i != '']
            input_type = 'variable_declaration'

        else:
            user_input = (' ' + i + ' ' if not i.isalnum() else i for i in user_input)
            user_input = [i for i in ''.join(user_input).split(' ') if i != '']
            if not self.balanced_brackets(user_input):
                print('Invalid expression')
                user_input = []
                input_type = 'wrong input'
                return user_input, input_type
            else:
                try:
                    user_input = [i if not i.isalpha() else str(self.variable_dictionary[i])
                                  for i in user_input]
                except KeyError:
                        print('Unknown variable')
                        user_input = []
            input_type = 'expression'

        return user_input, input_type

    @staticmethod
    def validate_identifier(user_input, printing=True):
        validate = user_input.isalpha()
        if not validate and printing:
            print('Invalid identifier')
        return validate

    @staticmethod
    def validate_assignment_general(user_input):
        validate = re.match(r'(^[0-9]+$)', user_input) or re.match(r'(^[a-zA-Z]+$)', user_input)
        if not validate:
            print('Invalid assignment')
        return validate

    @staticmethod
    def validate_assignment_number(user_input):
        validate = user_input.isnumeric()
        return validate

    @staticmethod
    def validate_assignment_letter(user_input):
        validate = user_input.isalpha()
        return validate

    def build_variable_dictionary(self, user_input):
        if not self.validate_identifier(user_input[0]):
            return False
        if not self.validate_assignment_general(user_input[1]):
            return False
        if self.validate_identifier(user_input[0], printing=False) and self.validate_assignment_number(user_input[1]):
            self.variable_dictionary[user_input[0]] = int(user_input[1])
        if self.validate_identifier(user_input[0], printing=False) and self.validate_assignment_letter(user_input[1]):
            if user_input[1] in self.variable_dictionary:
                self.variable_dictionary[user_input[0]] = self.variable_dictionary[user_input[1]]
            else:
                print('Unknown variable')

    def return_variable_value(self, user_input, printing=False):
        if user_input in self.variable_dictionary:
            if printing:
                print(self.variable_dictionary[user_input])
                return self.variable_dictionary[user_input]
            else:
                return self.variable_dictionary[user_input]
        else:
            print('Unknown variable')

    def run_input(self):
        user_input, input_type = self.parse_user_input()
        if len(user_input) == 0:
            user_input_to_calc = False
        elif input_type == 'command' and user_input[0] not in ('/exit', '/help'):
            print('Unknown command')
            user_input_to_calc = False
        elif user_input[0] == '/exit':
            print('Bye!')
            sys.exit()
        elif user_input[0] == '/help':
            print('The program calculates  the addition, multiplication, subtraction and division - operations')
            user_input_to_calc = False
        elif input_type == 'call_variable':
            user_input_to_calc = False
            validation = self.validate_identifier(user_input[0])
            if validation:
                self.return_variable_value(user_input[0], printing=True)
        elif input_type == 'variable_declaration' and len(user_input) > 2:
            print('Invalid assignment')
            user_input_to_calc = False
        elif input_type == 'variable_declaration' and len(user_input) == 2:
            self.build_variable_dictionary(user_input)
            user_input_to_calc = False
        else:
            user_input_to_calc = True

        return user_input_to_calc, user_input

    def calculate(self):
        while True:
            user_input_to_calc, user_input = self.run_input()
            if user_input_to_calc:
                result = Evaluate(Conversion(user_input).infixToPostfix()).evaluatePostfix()
                print(result)
            else:
                continue


Calculator().calculate()

