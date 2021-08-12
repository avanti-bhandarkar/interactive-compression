from collections import Counter
import string
import numpy as np
import pandas as pd
from decimal import *

getcontext().prec = 100

inputstr = input('Enter a Sequence: ')

# Convert the characters in line to lowercase 
inputstr = inputstr.lower()

# Remove punctuation marks from the line
inputstr = inputstr.translate(inputstr.maketrans('', '', string.punctuation))

res = Counter(inputstr)
print ('\n',str(res))
unsorted = list(res.keys())

sortres = {key: value for key, value in sorted(res.items(), reverse = True)}

M = len(sortres)
A = np.zeros((M,5),dtype=object)

reskeys = list(sortres.keys())
resvalue = list(sortres.values())
totalsum = sum(resvalue)

# Creating Table

A[M-1][3] = 0 
for i in range(M):
   A[i][0] = reskeys[i]
   A[i][1] = resvalue[i]
   A[i][2] = ((resvalue[i]*1.0)/totalsum)

i=0
A[M-1][4] = A[M-1][2]
while i < M-1:
   A[M-i-2][4] = A[M-i-1][4] + A[M-i-2][2]
   A[M-i-2][3] = A[M-i-1][4]
   i+=1

# creating a list of column names
column_values = ['Alphabet' , 'Frequency' , 'Probability' , 'Lower limit of interval', 'Upper limit of interval']

# creating the dataframe

df1 = pd.DataFrame(A, reskeys, column_values)
df1 = df1.set_index('Alphabet')

# displaying the dataframe
print(df1)

# Encoding

print('\n------- ENCODING -------\n')
strlist = list(inputstr)
LEnco = []
UEnco = []
CW = []

LEnco.append(0)
UEnco.append(1)
CW.append(1)

for i in range(len(strlist)):
  
    result = np.where(A == reskeys[reskeys.index(strlist[i])])

    addtollist = (LEnco[i] + (UEnco[i] - LEnco[i])*float(A[result[0],3]))
    addtoulist = (LEnco[i] + (UEnco[i] - LEnco[i])*float(A[result[0],4]))
    width = addtoulist - addtollist

    LEnco.append(addtollist)
    UEnco.append(addtoulist)

    CW.append(width) 

    tag = (LEnco[-1] + UEnco[-1])/2.0

string = list(i for i in inputstr)

B = np.zeros((len(strlist),1),dtype=object)

for i in range(len(strlist)):
   B[i][0] = string[i]

LEnco.pop(0)
UEnco.pop(0)
CW.pop(0)

values2 = np.transpose(np.array((LEnco, UEnco, CW),dtype=object))
values2 = np.hstack((B,values2))

# creating a list of column names
column_values2 = ['Alphabet','Lower limit of codeword' , 'Upper limit of codeword' , 'Width of codeword']
# creating the dataframe

df2 = pd.DataFrame(values2, string , column_values2)

df2 = df2.set_index('Alphabet')


# displaying the dataframe
print(df2)

print('\nThe Tag is: ', tag)

# Decoding

print('\n------- DECODING -------\n')
ltag = 0
utag = 1
decodedSeq = []
for i in range(len(inputstr)):
    numDeco = ((tag - ltag)*1.0)/(utag - ltag)
    for i in range(M):
        if (float(A[i,3]) < numDeco < float(A[i,4])):
            decodedSeq.append(str(A[i,0]))
            ltag = float(A[i,3])
            utag = float(A[i,4])
            tag = numDeco

print('The decoded sequence is \n')
print(''.join(decodedSeq))
