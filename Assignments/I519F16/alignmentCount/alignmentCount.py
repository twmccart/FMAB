from argparse import ArgumentParser
# we are using numpy for our matrices
import numpy as np

# Function to calculate number of possible alignments
# If double gaps are allowed

def alignCount_allowDoublegap(n,m) :
    # initial matrix full of zeros
    matrix = np.zeros([m+1,n+1],dtype=int) 
    #print "empty double gap matrix: ", matrix
    # fill first row and column with ones
    matrix[0,:] = np.ones(n+1)
    matrix[:,0] = np.ones(m+1)
    #print "ones double gap matrix: ", matrix
    ### Insert your code here
    ### dynamical programming loop to fill the rest of the matrix
    for i in range(1, m+1):
        for j in range(1, n+1):
            matrix[i,j] = matrix[i-1,j-1] + matrix[i-1,j] + matrix[i,j-1]
            #print "Filling ", i, ", ", j, " : "
            #print matrix

    # return the right bottom corner
    return matrix[-1][-1]


# Function to calculate number of possible alignments
# If double gaps are not allowed

def alignCount_forbidDoublegap(n,m) :
    # initial matrix full of zeros
    matrix = np.zeros([m+1,n+1],dtype=int) 
    #print "no double gaps"
    # fill first row and column with ones
    matrix[0,:] = np.ones(n+1)
    matrix[:,0] = np.ones(m+1)
   
    ### Insert your code here
    ### dynamical programming loop to fill the rest of the matrix
    for i in range(1, m+1):
        for j in range(1, n+1):
            #print "i= ", i, "  j= ", j
            horizontal = 0
            for k in range(1, j):
                #print "k= ", k
                horizontal += matrix[i-1, j-1-k]
                #print "horizontal= ", horizontal
            
            vertical = 0
            for k in range (1, i):
                #print "k= ", k
                vertical += matrix[i-1-k, j-1]
                #print "vertical= ", vertical
            matrix[i,j] = matrix[i-1,j-1] + horizontal + vertical
            #print "Filling ", i, ", ", j, " : "
            #print matrix
    # return the right bottom corner
    return matrix[-1][-1]

if __name__ == '__main__' :

    # Define program parameters
    parser = ArgumentParser(description='Reads a fasta sequence and counts k-mers')
    parser.add_argument('n', type=int, help='length of first sequence')
    parser.add_argument('m', type=int, help='length of second sequence')
    args = parser.parse_args()

    # Call the functions
    noDgaps = alignCount_forbidDoublegap(args.n, args.m)
    yesDgaps = alignCount_allowDoublegap(args.n, args.m)

    # Print the results
    print 'For sequences of length {} and {}, there are \n{} possible alignments if we do not allow double gaps \n{} alignments if we allow double gaps.'.format(args.n,args.m,noDgaps, yesDgaps)

