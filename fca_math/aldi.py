import numpy as np
from fca_math.diagrams import * 

def setrepmatrix(kk,ul = None):
   '''
   Returns the set representation matrix needed for
   additive line diagrams.
   '''
   if ul is None:
      ul = kk.uplist()
   srmatrix = np.zeros((len(ul),kk.gnum+kk.mnum))
   for c in range(len(ul)):
      for g in range(kk.gnum):
         if g in ul[c][0]:
            srmatrix[c,g] = 1.0
      for m in range(kk.mnum):
         if m not in ul[c][1]:
            srmatrix[c,kk.gnum+m] = 1.0
   return srmatrix

def srm_evaluate(kk,srmatrix,vectors,kknoc=None):
   '''
   Returns a normalized additive placement for given object- and attribute
   vectors. kk is noct actually used, only its number of concepts is needed.
   This can be provided as keywordargument kknoc.
   '''
   if kknoc is None:
      kknoc = kk.number_of_concepts()
   pos = Placement(kknoc)
   pos.xy = srmatrix @ vectors
   pos = pos.normalize()
   return(pos)

def column_gram_schmidt(A):
   '''
   Returns a matrix the columns of which form an orthonormal basis
   for the column space of A.
   '''
   B = np.zeros((len(A),0))
   for acolnum in range(A.shape[1]):
      projection = np.zeros((len(A),1))
      acol = A[:,acolnum:acolnum+1]
      if B.shape[1] > 0:
         for bcolnum in range(B.shape[1]):
            bcol = B[:,bcolnum:bcolnum+1]
            projection += np.dot(acol.T,bcol)*bcol
      newcol = acol - projection
      norm = np.linalg.norm(newcol)
      if norm > 1.e-05:
         newcol = newcol/norm
         B = np.column_stack((B,newcol))
   return B

def add_approx(pos,orthomatrix):
   '''
   Returns the placement which is closest to the input placement
   among the additive ones.
   '''
   newpos = Placement(pos.length)
   newpos.length = pos.length
   newpos.xy = orthomatrix @ (orthomatrix.T @ pos.xy)
   return newpos
            
