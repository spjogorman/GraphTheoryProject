#Sean O'Gorman 

def shunt(infix):

    #Dictionary of special characters and values representing precedence
    specials = {'*': 50, '.': 40, '|': 30}

    #Output String
    pofix = ""

    #Operator stack
    stack = ""

    #Loop through the input string one character at a time
    for c in infix:
        #If an open bracket, push to the stack
        if c == '(':
            stack = stack + c

        #If  closing bracket, pop from the stack, push to 
        #output until open bracket
        elif c == ')':
            while stack[-1] != '(':
                pofix = pofix + stack[-1]
                stack = stack[:-1] 
            stack = stack[:-1]

        #If it's an operator push to stack after popping lower or
        #equal precedence operators from top of stack into output
        elif c in specials:
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                pofix = pofix + stack[-1]
                stack = stack[:-1] 
            stack = stack + c

        #Regular characters are pushed immediately to the output
        else:
            pofix = pofix + c

    #Pop all remaining operators from stack to output
    while stack:
        pofix = pofix + stack[-1]
        stack = stack[:-1] 
    
    #Return postfix regex
    return pofix

print(shunt("(a.b)|(c*.d)"))