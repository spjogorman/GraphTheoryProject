#Sean O'Gorman

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
            nfastack.append(nfa(initial, accept))

        elif c == '*':
            #Pop the NFA off the stack
            nfa1 = nfastack.pop()

            #Create a new initial and accept state
            initial = state()
            accept = state()

            #Join the new initial state to NFA1's initial state
            #and the new accept state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept

            #Join the old accept state to the new accept state and
            #nfa1's initial state
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = nfa1.accept

            #Push new NFA to the stack
            nfastack.append(nfa(initial, accept))

        else:
            #Create a new initial and accept states
            accept = state()
            initial = state()

            #Join the initial state to thhe accept state using an 
            #arrow labelled c
            initial.label = c
            initial.edge1 = accept

            #Push new NFA to the stack
            nfastack.append(nfa(initial, accept))

    #Stack should only have a single nfa at this point
    return nfastack.pop()

print(compile("ab.cd.|"))