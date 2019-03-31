#Sean O'Gorman


def shunt(infix):
    """The Shunting Yard Algorithm for converting infix regular expressions 
    to postfix."""

    #Dictionary of special characters and values representing precedence
    specials = {'*': 50, '.': 40, '|': 30, '+': 20}

    #Output String
    pofix = ""
    #Operator stack
    stack = ""

    #Loop through the input string one character at a time
    for c in infix:
        #If an open bracket, push to the stack
        if c == '(':
            stack = stack + c
        #If  closing bracket, pop from the stack, push to output until open bracket
        elif c == ')':
            while stack[-1] != '(':
                pofix, stack  = pofix + stack[-1], stack[:-1] 
            stack = stack[:-1]
        #If it's an operator push to stack after popping lower or
        #equal precedence operators from top of stack into output
        elif c in specials:
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                pofix, stack  = pofix + stack[-1], stack[:-1] 
            stack = stack + c
        #Regular characters are pushed immediately to the output
        else:
            pofix = pofix + c

    #Pop all remaining operators from stack to output
    while stack:
        pofix, stack  = pofix + stack[-1], stack[:-1] 
    
    #Return postfix regex
    return pofix

class state:
    label = None
    edge1 = None
    edge2 = None

class nfa:
    initial = None
    accept = None

    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

def compile(pofix):
    """Compiles a postfix regular expression into an NFA."""

    nfastack = []

    for c in pofix:
        if c == '.':
            #Pop two NFA's off the stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            #Connect first accept state to the second initial state
            nfa1.accept.edge1 = nfa2.initial
            #Push new NFA to the stack
            newnfa = nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newnfa)
        elif c == '|':
            #Pop two NFA's off the stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            #Connect a new initial state, connect it to the 
            #initial states of two NFA's popped from the stack
            initial = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial
            #Create a new accept state, connect the previous two 
            #accept states to the new accept state
            accept = state()
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept
            #Push new NFA to the stack
            newnfa = nfa(initial, accept) 
            nfastack.append(newnfa)
        elif c == '*':
            #Pop the NFA off the stack
            nfa1 = nfastack.pop()
            #Create a new initial and accept state
            initial = state()
            accept = state()
            #Join the new initial state to NFA1's initial state and the new accept state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            #Join the old accept state to the new accept state and nfa1's initial state
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            #Push new NFA to the stack
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)
        elif c == '+':
            #Pop the NFA off the stack
            nfa1 = nfastack.pop()
            #Create a new initial and accept state
            initial = state()
            accept = state()
            #Join the new initial state to NFA1's initial state
            initial.edge1 = nfa1.initial
            #Join the old accept state to the new accept state and nfa1's initial state
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            #Push new NFA to the stack
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)
        else:
            #Create a new initial and accept states
            accept = state()
            initial = state()
            #Join the initial state to thhe accept state using an arrow labelled c
            initial.label = c
            initial.edge1 = accept
            #Push new NFA to the stack
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)

    #Stack should only have a single nfa at this point
    return nfastack.pop()


def followes(state):
    """Return the set of states that can reached from state following e arrows"""
    # Create a new set, with state as its only member
    states = set()
    states.add(state)

    # Check if the state has arrows labelled e from it
    if state.label is None:
        #Check if edge1 is a state
        if state.edge1 is not None:
            # If there's an edge1, follow it
            states |= followes(state.edge1)
        #Check if edge2 is a state
        if state.edge2 is not None:
            # If there's an edge2, follow it
            states |= followes(state.edge2)

    # Return the set of states
    return states


def match(infix, string):
    """Matches the string to infix regular expression."""

    # Shunt and compile the regular expression
    postfix = shunt(infix)
    nfa = compile(postfix)

    #The current set of states and the next set of states
    current = set()
    next = set()
    
    #Add the initial state to the current set
    current |= followes(nfa.initial)

    #Loop through each character in the string
    for s in string:
        #Loop through the current set of states
        for c in current:
            #Check if that state is labelled s.
            if c.label == s:
                # Add the edge1 state to the next set.
                next |= followes(c.edge1)
        #Set current to next, and clear out next
        current = next
        next = set()
        
    #Check if the accept state is in the set of current states
    return(nfa.accept in current)


userInfixes = []
userStrings = [""]

menuOption = eval(input("Press 1 to enter your own data, or 2 to run preloaded tests\n"))

if menuOption == 2:

    # Tests
    infixes = ["a+"]
    strings = ["", "a", "aaa", "ba", "bb"]

    """
    infixes = ["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "0.1*","(0.1)*"]
    strings = ["", "abc", "abbc", "abad", "abbbc", "01"]
    """

    for i in infixes:
        for s in strings:
            print(match(i, s), i, s)

elif menuOption == 1:
    numOfInfixes = eval(input("How many Infix expressions would you like to enter? (please use whole number, eg, 1,2,3..etc)\n"))

    for x in range(0, numOfInfixes):
        infixEntry = input("Please enter Infix expression e.g. a|b.b* (where '.' = and, '|' = or , '*' = one or more)\n")
        userInfixes.append(infixEntry)

    numOfStrings = eval(input("How many Strings would you like to evaluate? (please use whole number, eg, 1,2,3..etc)\n"))

    for x in range(0, numOfStrings):
        stringEntry = input("Please enter String (Empty String is included by default)\n")
        userStrings.append(stringEntry)

    for i in userInfixes:
        for s in userStrings:
            print(match(i, s), i, s)

