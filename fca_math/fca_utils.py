#
# Utilities used for the fca package
#
import os
from fca_math.closures import *

def lectic_smaller(A,B):
   '''
   Returns True if A ist lectically smaller than B,
   False otherwise.
   '''
   ls = False
   symdiff = (A - B) | (B - A)
   if symdiff != set():
      m = sorted(symdiff)[0]
   if m in B: ls = True
   return ls

def electic_smaller(A, B, listv = None):
   '''
   Experimental. Probably not needed.
   Returns True if A != B and of the elements in which
   A and B differ, the one with the smallest index in
   listv belongs to B.  False otherwise.
   '''
   ls = False
   symdiff = (A - B) | (B - A)
   if symdiff != set():
      if listv is None: m = min(symdiff)
      else: 
         ind = min([listv.index(i) for i in listv if i in symdiff])
         m = listv[ind]
   if m in B: ls = True
   return ls

def sstring(setvar):
   '''
   Returns a sorted string made from setvar.
   This is used to print sets with curly braces, but sorted.
   '''
   s = '{'
   for elem in sorted(setvar): s = s + str(elem) + ', '
   if setvar != set(): s = s[:-2]
   s = s + '}' 
   return s

def inversions(stringvar):
   ''' Returns the set of inversions of a string.
       Function is needed for Context.permutations(n).
   '''
   ivset = set()
   for i in range(len(stringvar)-1):
      for j in range(i+1,len(stringvar)):
         if ord(stringvar[i]) > ord(stringvar[j]):
            ivset.add((stringvar[i],stringvar[j]))
   return ivset

def intro():
   ''' First encounter with fca_math.'''
   os.system('cls' if os.name == 'nt' else 'clear')
   print()
   print('***************************************************',end="")
   print('***************************************************')
   print()
   print('       Welcome to the fca_math package, which contains basic Python\
 support for the mathematics ')
   print('       of Formal Concept Analysis. A documentation and a verbose introduction, called the ')
   print('       "fca_math enlightener" are freely available and probably included in your package.')
   print()
   print('       Here are some lines of code you may want to try:')
   print()
   print('>>> kk = Context(3,4)')
   print()
   print('       Assigns to kk a formal context with objects {0,1,2}, attributes {0,1,2,3}, and no incidences.')
   print()
   print('>>> kk.make_incident(1,2)')
   print()
   print('       Adds (1,2) to the incidence relation. Try print(kk) to check.')
   print()
   print('>>> kk.twenty_concepts()')
   print()
   print('       Prints up to 20 formal concepts of kk.')
   print()
   print('       For more possibilities check Figures 1, 2, 3 of the documentation, or read the enlightener.')
   print()
   print('***************************************************',end="")
   print('***************************************************')
   print()

   
 
