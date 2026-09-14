##################################################               
#   Implication and Implist class definition
##################################################
from fca_math.contexts  import *
from fca_math.fca_utils import *
from fca_math.closures  import *
import copy

##################################################
class Implication:
   '''
   An implication is a pair of sets.
   '''
   def __init__(self,P,C):
      if P == {}: P = set()
      self.premise = P.copy()
      self.conclusion = C.copy()

   def __str__(self):
      return sstring(self.premise)+' ==> '+ sstring(self.conclusion)
   
class Implist:
   def __init__(self,carrier):
      '''
      A list of implications, together with some additional data
      which support Algorithm 15 (LinClosure) of G & O.
      '''
      self.carrier,self.size = set_carrier(carrier)
      self.imp = []                # The list of implications
      self.empcons = set()         # Consequences of the empty set
      self.closure = Closureoperator(self.carrier, self.linclosure)
      self.count = []              # List of premise sizes
      self.list = [set() for m in range(self.size)] 
#     If m is an element of the premise of self.imp[index], then 
#     index is an element of self.list[m].
      
###############################
   def __str__(self):
      show = ''
      for impli in self.imp:
         nimpli = copy.copy(impli)
         show += Implication.__str__(nimpli) +'\n'
      return show  

   def named(self):
      '''
      Allows to print the implist with named implications.
      '''
      show = ''
      for impli in self.imp:
         nimpli = copy.copy(impli)
         nimpli = self.named_imp(nimpli)
         show += Implication.__str__(nimpli) +'\n'
      return show   

##################################################
   def addimp(self, PC):
      ''' Appends an implication to an implist''' 
      if PC.premise <= self.empcons:
         self.empcons |= PC.conclusion
      (self.imp).append(PC)
      (self.count).append(len(PC.premise))
      for m in PC.premise:
         self.list[m].add(len(self.imp)-1)

##################################################
   def addpc(self,P,C):
      '''
      Short version of addimp when premise and conclusion
      are given.
      '''
      self.addimp(Implication(P,C))

##################################################
   def named_imp(self,impli):
      ''' Replace unnamed implication by named.'''
      return Implication(named_set(self.carrier,impli.premise),\
                         named_set(self.carrier,impli.conclusion))
   
   def denamed_imp(self,impli):
      ''' Replace named implication by unnamed.'''
      return Implication(denamed_set(self.carrier,impli.premise),\
                         denamed_set(self.carrier,impli.conclusion))
   
   def addnimp(self,PC):
      '''Appends a named implication.'''
      self.addimp(self.denamed_imp(PC))
      
##################################################
   def linclosure(self,previous):
      ''' ALgorithm 15 in G & O.'''
      localcount = self.count.copy()
      X = previous.copy()
      X |= self.empcons      
      update = X.copy()
#
      while update != set():
         for m in update: break           # Choose some m from update
         update.remove(m)
         for impnr in self.list[m]:
            localcount[impnr] -= 1
            if localcount[impnr] == 0:
               add = self.imp[impnr].conclusion - X
               X |=  add
               update |= add
      return X

##################################################
   def iclosure(self,inset,dontuse=set()):
      '''
      Closure with respect to an implication list, different from
      linclosure. The optional parameter dontuse allows to not use
      all implications. This is useful e.g. when checking if the
      given list is redundant.
      '''
      outset = inset.copy()
      notuse = dontuse.copy()
      select = set(range(len(self.imp))) - dontuse
      while True:
         stable = True
         for impnr in select:
            if impnr not in notuse:
               if self.imp[impnr].premise <= outset:
                  outset |= self.imp[impnr].conclusion
                  stable = False
                  notuse.add(impnr)
         if stable: break         
      return outset

###############################
   def minimal_cover(self):
      ''' Algorithm 18 in Ganter & Obiedkov '''
      for impnr,impli in enumerate(self.imp):
         impli.conclusion = \
            self.iclosure(impli.premise|impli.conclusion,dontuse={impnr})
      newlist = Implist(self.carrier)
      for impnr,impli in enumerate(self.imp):
         A = impli.premise
         newA = newlist.iclosure(A)
         newA = self.iclosure(A,dontuse={impnr})
         if newA != impli.conclusion:
            newlist.addimp(Implication(newA,impli.conclusion))
      return newlist

###############################
   def first_closure(self,avoid=set(),contain=set()):
      ''' First set closed under the implications.'''
      if avoid | contain == set():  
         return self.empcons
      else:
         return self.closure.first_closure(avoid, contain)

   def next_closure(self,previous):
      return self.closure.next_closure(previous)
 
##################################################
   @classmethod
   def make_addsat(cls,n):
      ''' Generates the implications for additively saturated
      subsets of {1,2,...,n}'''   
      impl = Implist([i for i in range(1,n+1)])
      for g in range(1,n+1):
         for h in range(g,n+1):
            if g + h <= n: impl.addnimp(Implication({g,h},{g+h}))
      return impl               

##################################################
   def human_readable(self,buddies=set()):
      '''
      Returns an equivalent basis which we assume is more
      humanly-readable. The optional argument (buddies)
      allows to name preferred elements. These only play a role
      when there equivalent elements.
      '''
      worklist = []
      self.empcons = self.iclosure(set())
#     Find representatives for the equivalence classes 
      unclassified = set(range(self.size)) - self.empcons - buddies
      equiclass = []
      representative = []
      for b in buddies - self.empcons:
         classb = set()
         for a in self.iclosure({b}):
            if b in self.iclosure({a}):
               classb.add(a)
         representative.append(b)
         equiclass.append(classb)
         unclassified -= classb
      while unclassified != set():
         for b in unclassified: break
         classb = set()
         for a in self.iclosure({b}):
            if b in self.iclosure({a}):
               classb.add(a)
         representative.append(b)
         equiclass.append(classb)
         unclassified -= classb
      reps = set(representative)
#     replace elements by their representatives 
      for impli in self.imp:
         P = impli.premise.copy()
         C = impli.conclusion.copy()
         for e in reps:
            indx = representative.index(e)
            if P & equiclass[indx] != set():
               P |= {e} 
            if C & equiclass[indx] != set():
               C |= {e} 
         P &= reps
         C &= reps
#        make conclusion disjoint from premise
         C -= P
#        remove consequences of 1-element sets
         done = set()
         while P - done != set():            
            for p in P - done: break
            p_clo = self.iclosure({p})
            done |= p_clo 
            P -= (p_clo - {p})
         done = set()
         while C - done != set():            
            for p in C - done: break
            p_clo = self.iclosure({p})
            done |= p_clo 
            C -= (p_clo - {p})
         worklist.append(Implication(P,C))
#     add cycles through equivalence classes         
      for i in range(len(equiclass)):
         if len(equiclass[i]) > 1:
            equilist = list(equiclass[i])
            for j in range(len(equilist)-1):
               worklist.append(Implication({equilist[j]},{equilist[j+1]}))
            worklist.append(Implication({equilist[-1]},{equilist[0]}))
#     add implication with empty premise, if needed            
      if self.iclosure(set()) != set():
         worklist.append(Implication(set(),self.iclosure(set())))
#     Merge implications with equal premise
      worklist = merge_imps(worklist)
      worklist = remove_redundant(worklist)
      hr = Implist(self.carrier)      
      for imp in worklist:
         if imp.premise == set():
            hr.addimp(imp)
            break
      for imp in worklist:
         if len(imp.premise) == 1:
            hr.addimp(imp)
      for imp in worklist:
         if len(imp.premise) > 1:
            hr.addimp(imp)
      return hr
         
def iclose(liste,inset,dontuse=set()):
      '''
      Closure with respect to a list of implications, different from
      linclosure. The optional parameter dontuse allows to not use
      all implications. This is useful e.g. when checking if the
      given list is redundant.
      '''
      outset = inset.copy()
      notuse = dontuse.copy()
      select = set(range(len(liste))) - dontuse
      while True:
         stable = True
         for impnr in select:
            if impnr not in notuse:
               if liste[impnr].premise <= outset:
                  outset |= liste[impnr].conclusion
                  stable = False
                  notuse.add(impnr)
         if stable: break         
      return outset

def merge_imps(liste):
   '''
   Modifies a given list of implications (not an Implist!) by 
   merging those with the same premise.
   '''
   i = 0
   while i < len(liste)-1:
      P = liste[i].premise
      popset = set()
      joinset = set()
      for j in range(i+1,len(liste)):
         if P == liste[j].premise:
            popset.add(j)
            joinset |= liste[j].conclusion
      if popset != set():
         liste[i].conclusion |= joinset
         liste = [x for x in liste if liste.index(x) not in popset]
      i += 1
   return liste

def remove_redundant(liste):
   '''
   Removes implications from liste which follow from other ones.
   '''
   popset = set()
   usenot = set()
   for impnr in range(len(liste)):
      usenot = popset | {impnr}
      premclose = iclose(liste,liste[impnr].premise,usenot)
      if premclose >= liste[impnr].conclusion:
         popset |= {impnr}
   liste = [x for x in liste if liste.index(x) not in popset]
   return(liste)

         
   
      
      
     
      
   
