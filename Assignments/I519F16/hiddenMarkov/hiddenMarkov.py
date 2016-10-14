from sys import argv
from numpy import zeros, argmax

# viterbi will return the most likely hiden state sequence. 

def viterbi(initial, transition, emission, observed) :
    
    # infer hidden states
    states = initial.keys()

    # initialize matrices
    score = zeros([len(states), len(observed)])
    trace = zeros([len(states), len(observed)], dtype=int)
    
    # forward pass
    for i, obs in enumerate (observed) :
        for j, st in enumerate (states) :
            ### Insert your code here
            ### Goal : implement forward pass of Viterbi algorithm
            ### Fill the score and trace matrices
            #print "i, obs= ", i, ", ", obs
            #print "j, st= ", j, ", ", st
            
            if i == 0 :
                ### Fill the first column here
                score[j,i] = initial[st]*emission[st][obs]
                trace[j,i] = 0
            else :
                ### Fill the rest of the columns here
                #score_choices = []
                #for k in range(0, len(states)):
                    #print "i=", i
                    #print "j=", j
                    #print "k=", k
                    #print "score[k,i-1]=", score[k,i-1]
                    #print "transition[states[k]][st]=", transition[states[k]][st]
                    #print "emission[st][obs]=", emission[st][obs]
                    #print "score_choice=", score[k,i-1]*transition[states[k]][st]*emission[st][obs]
                    #score_choices.append(score[k,j-1]*transition[states[k]][st]*emission[st][obs])
                #print "Score choices: ", score_choices
                score[j,i] = max(score[k,i-1]*transition[states[k]][st]*emission[st][obs] for k in range(0, len(states)))
                ## this is a brilliant use of a lambda function, because argmax() does not work on iterables
                trace[j,i] = max(range(0, len(states)), key=lambda k: score[k,i-1]*transition[states[k]][st]) ## It is not necessary to include "*emission[st][obs]" because it will be constant for all k
            #print "score"
            #print score
            #print "trace"
            #print trace
    # trace back
    z = argmax(score[:,-1]) #score is an array, not a list
    hidden = states[z]

    for i in range(1,len(observed))[::-1] :
        z = trace[z,i]
        hidden += states[z]

    # return REVERSED traceback sequence
    return hidden[::-1]

if __name__ == '__main__' :

    # initial probabilities of (F)air and (B)iased coins
    initial = {'F':0.5, 'B':0.5}

    # transition probabilities btw (F)air and (B)iased coins
    transition = {'F':{'F':0.8, 'B':0.2}, 'B':{'F':0.2, 'B':0.8} }

    # emmision probabilites from (F)air and (B)iased coins
    emission = {'F':{'H':0.5, 'T':0.5}, 'B':{'H':0.2, 'T':0.8} }

    # observed sequence is the only input to the program
    sequence = argv[1]

    print viterbi (initial, transition, emission, sequence)
    

