#
# Python functions supplementing the fca package: Bonds, closed relations
#
from fca_math.contexts import *
from fca_math.implications import *

def close_bond(kk1,kk2,J):
   ''' Requires as input three formal contexts kk1, kk2, J,
   where J has the same object set as kk1 and the same attribute
   set as kk2.
   The function returns the smallest bond between kk1 and kk2 which
   contains the incidene relation of J, again in form of a context.'''
   B = J.copy()
   change = True
   while change:
      change = False
      for g in range(kk1.gnum):
         Vorher = B.gintent[g].copy()
         Nachher = kk2.close_intent(Vorher)
         if Nachher != Vorher:
            change = True
            for m in Nachher - Vorher:
               B.make_incident(g,m)
      for m in range(kk2.mnum):
         Vorher = B.mextent[m].copy()
         Nachher = kk1.close_extent(Vorher)
         if Nachher != Vorher:
            change = True
            for g in B.mextent[m] - Vorher:
               B.make_incident(g,m)
   return B   

def skeleton_blockrel(kk):
   '''
   Returns the smallest block relation containing
   the neighbourhood relation.
   '''
   ua = kk.up_arrows()
   J = kk.copy()
   for g in range(kk.gnum):
      for m in range(kk.mnum):
         if ua.isincident(g,m): J.make_incident(g,m)
   B = close_bond(kk,kk,J)
   return B

def spine(kk):
   '''
   Returns the closed relation for the sublattice consisting of
   all formal concepts which are comparable to all other ones.
   '''
   sp = Context(kk.gnum,kk.mnum)
   def isempty(cc,A,B):
      result = False
      broken = False
      for g in A:
         for m in B:
            if kk.isincident(g,m):
               broken = True
               break
      if not broken: result = True
      return result
#   
   E = kk.first_extent()
   while E is not None:
      Eprime = kk.make_intent(E)
      F = set(range(kk.gnum)) - E
      Fprime = set(range(kk.mnum)) - Eprime
      if isempty(kk,F,Fprime):
         for g in E:
            for m in Eprime:
               sp.make_incident(g,m)
      E = kk.next_extent(E)    
   return sp   

def bond_implist(kk1,kk2):
   bcarrier=[(g,m) for g in range(kk1.gnum) for m in range(kk2.mnum)]
   bilist = Implist(bcarrier)
   il1 = kk1.dual().canonical_basis()
   for imp in il1.imp:
      for m in range(kk2.mnum):
         Pm = {(g,m) for g in imp.premise}
         Cm = {(g,m) for g in imp.conclusion}
         bilist.addpc(Pm,Cm)
   for imp in kk2.canonical_basis():
      for g in range(kk1.gnum):
         Pg = {(g,m) for m in imp.premise}
         Cg = {(g,m) for m in imp.conclusion}
         bilist.addpc(Pg,Cg)
   return bilist, bcarrier
