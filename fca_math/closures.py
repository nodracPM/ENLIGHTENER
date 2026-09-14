############################################################
#
#  Bernhard Ganter's Python programs for closure operators, 
#  mainly the next_closure algorithm. No FCA is required for
#  this; variants of these functions for formal contexts are
#  contained in other modules.
#
#  The class Closureoperator requires two arguments, the closure
#  operator and the set on which it operates. The set must
#  be given in form of its size or by a list (carrier) of
#  its elements. If the "carrier" parameter is an integer,
#  it is assumed that the list is [0,1,...,size - 1].
#
#  There is a class attribute (search) which allows to restrict
#  the search index used in next_closure to a given interval.
#
############################################################
from fca_math.carrier import *

class Closureoperator:
   def __init__(self, carrier, operator):
      self.operator  = operator
      self.carrier,self.size = set_carrier(carrier)
      self.mustcontain = set()   
      self.search   = [0,self.size]

   def avoid_contain(self,avoid = set(), contain = set()):
      mustcontain = self.operator(contain)
      if not mustcontain.isdisjoint(avoid) :
         print('Bad Avoid-Contain sets.')
         return None      #     An exception would be better
      rest = (set(self.carrier) - mustcontain) - avoid
      ac = len(avoid) + len(mustcontain)
      self.search = [ac, ac + len(rest)]
      self.mustcontain = mustcontain
      self.carrier = [self.carrier[a] for a in sorted(avoid)] +\
            [self.carrier[c] for c in sorted(mustcontain)] +\
            [self.carrier[r] for r in sorted(rest)]

   def first_closure(self):
      '''
      Returns the closure of the set mustcontain, which is empty
      by default.
      '''
      return self.operator(self.mustcontain)

   def next_closure(self,previous):
      '''
      Returns the next closure after prevoius.
      '''
      menge = previous.copy()
      ii = self.search[1]
      success = False
      while (ii > self.search[0]) and (not success):
         ii -= 1
         if ii in menge:
            menge.remove(ii)
         else:
            menge.add(ii)
            huelle = self.operator(menge)
            segment = huelle & set(range(ii))
            success = (segment <= menge)
            if success:
               menge = huelle
            else:
               menge.remove(ii)
      if success: return menge
      else: return None 
   
   def is_join_irreducible(self,i):
      ''' Is probably not needed.'''
      C = self.operator({self.carrier[i]})
      if len(C) == self.size: return False
      D = set()
      for j in range(self.size):
         if j != i:
            E = self.operator({self.carrier[j]})
            if E <= C:
               if E == C :
                  if j < i: return False
               else: D |= E
      if D < C: return True
      else: return False

   def is_meet_irreducible(self,closedset):
      star = set(range(self.size))
      diff = star - closedset
      for g in diff:
         star = star & self.operator(closedset | {g})
      if star == closedset: return False   
      else: return True

   def make_context(self):
      from fca_math.contexts import Context
      mlist = []
      closedset = self.first_closure()
      while closedset is not None:
         if self.is_meet_irreducible(closedset):
            mlist.append(closedset.copy())
         closedset = self.next_closure(closedset)
      gnum = self.size
      mnum = len(mlist)
      kk = Context(gnum,mnum)
      for g in range(gnum):
         kk.gname[g] = str(self.carrier[g])
      for m in range(mnum):
         kk.mname[m] = str(mlist[m])
      for g in range(gnum):
         for m in range(mnum):
            if self.carrier[g] in named_set(self.carrier,mlist[m]):
               kk.make_incident(g,m)
      return kk

   @classmethod
   def from_implist(cls,impl):
      return Closureoperator(impl.carrier, impl.linclosure)
   
##################################################
   def extremal_points(self,inset):
      expoints = set()
      closedset = self.operator(inset)
      for g in closedset:
         if not (self.operator(closedset - {g}) == closedset):
            expoints.add(g)
      return expoints      

##################################################
   def next_mingen(self,A,k = 100):
      for e in range(self.size-1,-1,-1):
         if e in A:
            A.remove(e)
         elif len(A) < k:
            B = A | {e}
            for b in B:
               if self.operator(B-{b}) == self.operator(B):
                  break
            else: return B
      return None

# ##################################################
#    def next_mingen(self,A,k = 100):
#       for e in range(self.size-1,-1,-1):
#          if e in A:
#             A.remove(e)
#          elif len(A) < k:
#             B = A | {e}
#             sccss = True
#             for b in B:
#                if self.operator(B-{b}) == self.operator(B):
#                   sccss = False
#                   break
#             if sccss: return B
#       return None

   
            



