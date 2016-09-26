from argparse import ArgumentParser
from random import random
import sys

# Function to generate initial (marginal) probabilities from conditional probabilities
def generate_init_prob(cond_prob) :
    initial=dict('A', 0; 'T', 0; 'C', 0; 'G', 0)

    ### Insert your code here
    ### Goal : get marginal probabilities for A,C,T,G
    ### e.g. P(A) from P(A|A), P(A|T), P(A|C), P(A|G)
    for key in cond_prob.keys():
        initial[key[-1:]] += cond_prob[key]

    return initial
    
def generate_conditional_probabilities_dict(cond_prob):
    subkmer_probability_sums={}
    usable_conditional_probabilities={}
    for kmer in cond_prob:
        subkmer = kmer[:-1]
        if subkmer in subkmer_probability_sums:
            subkmer_probability_sums[subkmer] += cond_prob[kmer]
        else:
            subkmer_probability_sums[subkmer] = cond_prob[kmer]
    for kmer in cond_prob:
        subkmer = kmer[:-1]
        new_nucleotide = kmer[-1:]
        if subkmer in usable_conditional_probabilities:
            usable_conditional_probabilities[subkmer[new_nucleotide]] = cond_prob[kmer]/subkmer_probability_sums[subkmer]
        else:
            usable_conditional_probabilities[subkmer] = {}
            usable_conditional_probabilities[subkmer[new_nucleotide]] = cond_prob[kmer]/subkmer_probability_sums[subkmer]

def generate_markov(length, cond_prob, order=1) :

    sequence=''

    # Generate initial probabilities from conditional probabilities
    init_prob = generate_init_prob(cond_prob)

    ### Insert your code here
    ### Goal 1 : generate first character
    for i in range(order) :
        dice = random()
        limit=0
        # We divide [0,1) interval according to probabilities of each nucleotide
        for nuc in init_prob :
            limit += init_prob[nuc]
            # We add the letter that dice hits
            if dice<limit :
                sequence += nuc
                limit = 0
                # Roll another dice for the next nucleotide
                break

    assert len(sequence) == order, 'First character was not generated'

    ### Insert your code here
    ### Goal 2 : generate rest of the sequence
    useful_probabilities=generate_conditional_probabilities_dict(cond_prob)
    for i in range(length-1) :
        subkmer=sequence[-order:]
        relevant_probabilities = useful_probabilities[subkmer]
        # Get a random number in [0,1)
        dice = random()
        limit=0
        # We divide [0,1) interval according to probabilities of each nucleotide
        for nuc in useful_probabilities :
            limit += useful_probabilities[nuc]
            # We add the letter that dice hits
            if dice<limit :
                seq_string += nuc
                limit = 0
                # Roll another dice for the next nucleotide
                break

    assert len(sequence) == length, 'Sequence is wrong length'

    return sequence


if __name__ == '__main__' :

    # Define program parameters
    parser = ArgumentParser(description='Generates a random sequence using a markov chain')
    parser.add_argument('-o', '--order', type=int, default=1, help='order of markov chain')
    parser.add_argument('-l', '--length', type=int, default=10, help='length of sequences')
    parser.add_argument('-n', '--number', type=int, default=1, help='number of sequences')
    args = parser.parse_args()

    # Read model parameters from stdin
    cond_prob = dict()
    for line in sys.stdin :
        kmer, prob = line.strip().split()
        cond_prob[kmer] = float(prob)

    # Print n random sequences to stdout
    for i in range(args.number) :
        print generate_markov (args.length, cond_prob)
