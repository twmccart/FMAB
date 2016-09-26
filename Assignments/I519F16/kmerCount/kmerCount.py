from Bio import SeqIO
from argparse import ArgumentParser
import itertools
## Program to count kmers in a fasta file

# This function should count kmers and return the result in a dictionary.
# !! All possible kmers should be present in the dictionary,
# Even if they do not exist in the sequence.

def count_kmers(sequenceList, k=2) :
    kmer_count = dict()
    ## make an iterable that will produce all possible kmers of length k
    kmers_iterable = itertools.product('ATCG', repeat=k)
    #print "kmers:"
    #for kmer in kmers_iterable:
        #print ''.join(kmer)
    ## Add all kmers to dict
    for kmer in kmers_iterable:
        kmer_count[''.join(kmer)] = 0
        

    # Note that you get a sequence list instead of a single sequence
    # Looping over all sequences...
    for sequence in sequenceList :
        while len(sequence) >= k:
            ## use slice indices to identify kmer
            kmer_count[sequence[:k]] += 1
            ## remove first letter (changes identity of variable 'sequence')
            sequence = sequence[1:]

    return kmer_count

# This function should normalize kmer counts to provide conditional probabilities
# The last letter of the kmer is conditioned on the first k-1

def normalize_counts(kmer_count, k=2) :
    kmer_prob = dict()
    subkmer_count = {}
    subkmers_iterable = itertools.product('ATCG', repeat=(k-1))
    for subkmer in subkmers_iterable:
        subkmer_count[''.join(subkmer)] = 0
    #print "subkmer_count: ", subkmer_count

    for key in kmer_count.keys():
        #print "key: ", key
        #print "key[:k-1] : ", key[:k-1]
        #print "before subkmer_count[key[:k-1]] : ", subkmer_count[key[:k-1]]
        ## Front bit of each kmer is used as the key for a subkmer_count
        subkmer_count[key[:k-1]] += kmer_count[key]
    #print "subkmer_count: ", subkmer_count
    for key in kmer_count.keys():
        #print "key: ", key
        #print "kmer_count[key]: ", kmer_count[key]
        #print "subkmer_count[key[:k-1]]: ", subkmer_count[key[:k-1]]
        kmer_prob[key] = (float(kmer_count[key])/subkmer_count[key[:k-1]])
    
    return kmer_prob

if __name__ == '__main__' :

    # Define program parameters
    parser = ArgumentParser(description='Reads a fasta sequence and counts k-mers')
    parser.add_argument('-i', '--infile', help='input file in fasta format')
    parser.add_argument('-k', type=int, default=2, help='k as in k-mer')
    args = parser.parse_args()

    # Read training sequences from fasta file
    sequences = [str(record.seq) for record in SeqIO.parse(args.infile, 'fasta') ]

    # Count all the kmers in these sequences
    counts = count_kmers(sequences,args.k)

    # Normalize counts to get conditional probabilities
    probs = normalize_counts(counts)

    # Print the resulting conditional probabilities
    for kmer in probs :
        print kmer, probs[kmer]

    # Note that we print everything to stdout rather than write to a file
    # User has the option to redirect to a file
