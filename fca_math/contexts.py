##################################################
#     Bernhard Ganter's Python package fca
##################################################
from fca_math.fca_utils import *
from fca_math.carrier   import *
from fca_math.closures  import *
from fca_math.implications import *
import sys
##################################

##################################
# Utilities first, no indentation
##################################
def cxt_typein(gnames = None, mnames = None):
   '''
   Used to type in a formal context. When invoked, the function
   will ask for size, names, and incidences of the formal context,
   which eventually is returned. The incidences must be given in
   row-wise (i.e., as object intents), in the form xx.x.xx.
   '''
   if gnames is None:
      gnames = int(input('Number of objects: '))
   if mnames is None:
      mnames = int(input('Number of attributes: '))
   kk = Context(gnames,mnames)
   kk.name = input('Context name: ')
   for m in range(kk.mnum):
      txt = input(f'Name of attribute {str(m)} (default = {kk.mname[m]}): ')
      if txt != '':
         kk.mname[m]=txt
   for g in range(kk.gnum):
      txt = input(f'Name of object {str(g)} (default = {kk.gname[g]}): ')
      if txt != '':
         kk.gname[g]=txt
      kk.set_intent(g,input('Intent of this object: '))
   return kk
         
###############################
def cxt_read(cxtname):
   ''' An alternative name for a class method.'''
   kk = Context.read(cxtname)
   return kk
         
###############################
def cxt_predefined(cxtfilename):
   ''' A variant for predefined contexts.'''
   kk = Context.read(cxtfilename,cxtpath='contexts/predefined/')
   return kk

#############################################
#    Formal context class definition init
#
#    An empty context of size (g,m) is obtained
#    by invoking  variable =  Context(g,m)
##############################################
class Context:
   def __init__(self,gcarrier,mcarrier):
      self.gname,self.gnum = set_carrier(gcarrier)
      self.mname,self.mnum = set_carrier(mcarrier)
      self.G = range(self.gnum)
      self.M = range(self.mnum)
      self.name = ''
      self.gintent = [set() for i in range(self.gnum)]
      self.mextent = [set() for i in range(self.mnum)]
      self.gclosure = Closureoperator(self.gname, self.close_extent)
      self.mclosure = Closureoperator(self.mname, self.close_intent)
      self.placement = None

#############################################
#    Formal context class definition str and repr
#############################################
   def __str__(self):
      ''' Prints context in LaTeX fca.sty format.'''
      anz = f'\\begin{{cxt}} %  {str(self.gnum)} object'
      if self.gnum != 1: anz = anz + 's'
      anz = anz + f', {str(self.mnum)} attribute'
      if self.mnum != 1: anz = anz + 's'
      anz = anz + '\n'
      anz = anz + '\\cxtName{'+self.name+'}\n'
      if (self.mnum > 0) and (len(self.mname[0]) > 1):
         for m in range(self.mnum):
            anz = anz + f'\\atr{{{self.mname[m]}}} % {str(m)} \n'
      else:      
         for m in range(self.mnum):
            anz = anz + f'\\att{{{self.mname[m]}}} % {str(m)} \n'
      for g in range(self.gnum):
         anz = anz + f'\\obj{{{self.xdot_out(g)}}}{{{self.gname[g]}}}'
         anz = anz + f'  % {str(g)} \n'
      anz = anz + '\\end{cxt}\n'
      return anz

#############################################
   def __repr__(self):
      ''' Prints context with arrows in LaTeX fca.sty format.
          To invoke, use print([kk]) instead of print(kk).   '''
      def xdot_arrows(ua,da,g):
         """Makes a string 'x..x.x' from object intent, with u,d,b."""     
         outstr = ''
         for m in range(self.mnum):
            if self.isincident(g,m): outstr = outstr + 'x'
            else:
               if ua.isincident(g,m):
                  if da.isincident(g,m): outstr = outstr + 'b'
                  else: outstr = outstr + 'u'
               else:
                  if da.isincident(g,m):  outstr = outstr + 'd'
                  else: outstr = outstr + '.'
         return outstr
      
      ua = self.up_arrows()
      da = self.down_arrows()
      anz = f'\\begin{{cxt}} %  {str(self.gnum)} object'
      if self.gnum != 1: anz = anz + 's'
      anz = anz + f', {str(self.mnum)} attribute'
      if self.mnum != 1: anz = anz + 's'
      anz = anz + '\n'
      anz = anz + '\\cxtName{'+self.name+'}\n'
      if (self.mnum > 0) and (len(self.mname[0]) > 1):
         for m in range(self.mnum):
            anz = anz + f'\\atr{{{self.mname[m]}}} % {str(m)} \n'
      else:      
         for m in range(self.mnum):
            anz = anz + f'\\att{{{self.mname[m]}}} % {str(m)} \n'
      for g in range(self.gnum):
         anz = anz + f'\\obj{{{xdot_arrows(ua,da,g)}}}{{{self.gname[g]}}}'
         anz = anz + f'  % {str(g)} \n'
      anz = anz + '\\end{cxt}\n'
      return anz

################################################
# Formal context file operations read and write
################################################
   @classmethod
   def read(cls,cxtfname,cxtpath='contexts/user/'):
      '''Reads a context from a file.'''     
      filename=cxtfname
      if (len(filename)>4) and (filename[-4:]=='.cxt'):
         filename=filename[:-4]
      with open(cxtpath+filename+'.cxt') as cxtfile:
         cxtfile.readline()
         nom = cxtfile.readline()[:-1]
         if (nom == '') or (nom == ' '):
            nom=filename
         xxgnum=int(cxtfile.readline()[:-1])
         xxmnum=int(cxtfile.readline()[:-1])
         cxtfile.readline()
         xx=cls(xxgnum,xxmnum)    
         xx.name=nom
         for i in range(xx.gnum):
            xx.gname[i] = cxtfile.readline()[:-1]
         for i in range(xx.mnum):
            xx.mname[i] = cxtfile.readline()[:-1]
         for i in range(xx.gnum):
            xx.set_intent(i,cxtfile.readline())
         return xx
      
   @classmethod
   def from_book(cls,cxtname):
      ''' Reads a context from the GW book. '''
      try:
         xx = Context.read(cxtname,'contexts/gwbook/GW2-')
         return xx
      except FileNotFoundError:
         print('No such figure in the GW-book. Available cxtnames are:')
         print('Fig1.1,  Fig1.5,  Fig1.10a, Fig1.11, Fig1.14, Fig1.17,')
         print('Fig1.23, Fig1.26, Fig2.4,   Fig2.9,  Fig2.15, Fig2.20,')
         print('Fig3.2,  Fig3.3a, Fig3.3b,  Fig3.3c, Fig3.10, Fig4.4,')
         print('Fig4.8,  Fig6.1,  Fig6.3,   Fig6.6,  Fig8.3.')
         return None
      
#   @classmethod

###############################
   def write(self,cxtfilename):
      '''Writes a context to a file'''
      if (len(cxtfilename) < 5) or (cxtfilename[-4:]!='.cxt'):
         cxtfilename += '.cxt'
      cxtpathname = 'contexts/user/'   
      with open(cxtpathname+cxtfilename,'w') as f:
         f.write('B'+'\n')
         f.write(self.name+'\n')
         f.write(str(self.gnum)+'\n')
         f.write(str(self.mnum)+'\n\n')
         for i in range(self.gnum):
            if self.gname[i]=='':
               self.gname[i]='g'+str(i)
            f.write(self.gname[i]+'\n')
         for i in range(self.mnum):
            if self.mname[i]=='':
               self.mname[i]='m'+str(i)
            f.write(self.mname[i]+'\n')
         for i in range(self.gnum):
            for j in range(self.mnum):
               if self.isincident(i,j):
                  f.write('x')
               else: f.write('.')
            f.write('\n')
              
#############################################
#    Formal context manipulation methods
#############################################
   def gindex(self,g):
      gout = g
      if isinstance(g,str): gout = self.gname.index(g)
      return(gout)
   
   def mindex(self,m):
      mout = m
      if isinstance(m,str): mout = self.mname.index(m)
      return(mout)

   def make_incident(self,g,m):
      '''Adds (g,m) to the incidence relation.'''
      if isinstance(g,set): gset = g
      else: gset = {g}
      if isinstance(m,set): mset = m
      else: mset = {m}
      for g in gset:
         for m in mset:
            self.gintent[self.gindex(g)].add(self.mindex(m))
            self.mextent[self.mindex(m)].add(self.gindex(g))
          
   def make_nonincident(self,g,m):
      if isinstance(g,set): gset = g
      else: gset = {g}
      if isinstance(m,set): mset = m
      else: mset = {m}
      '''Removes (g,m) from the incidence relation.'''
      for g in gset:
         for m in mset:
            self.gintent[self.gindex(g)].discard(self.mindex(m))
            self.mextent[self.mindex(m)].discard(self.gindex(g))
          
   def isincident(self,g,m):
      '''True if (g,m) is in the gintent relation'''
      if self.mindex(m) in self.gintent[self.gindex(g)]: return True
      else: return False

   def empty(self):
      ''' Returns an empty context of the size of self '''
      empty = Context(self.gnum,self.mnum)
      return empty

   def set_intent(self,g,msetcode):
      """Input an object intent. msetcode may be
      a set or a string of 'x' and '.'. 
      """
      mset = setinput(msetcode)
      for m in range(self.mnum):
         if (m in mset) or (self.mname[m] in mset):
            self.make_incident(g,m)
         else: self.make_nonincident(g,m)

   def gflip(self,g_in,h_in):
      '''Interchanges two object numbers.'''
      g = self.gindex(g_in)
      h = self.gindex(h_in)
      newcontext = self.copy()
      oldgintent = self.xdot_out(g)
      oldhintent = self.xdot_out(h)
      newcontext.set_intent(g,oldhintent)
      newcontext.set_intent(h,oldgintent)
      newcontext.gname[h] = self.gname[g]
      newcontext.gname[g] = self.gname[h]
      return newcontext

   def mflip(self,m,n):
      '''Interchanges two attribute numbers.'''
      return self.dual().gflip(m,n).dual()

   def add_object(self,gintent,name=''):
      '''Adds an object with intent gintent. "name" 
      is optional parameter for the object's name.'''
      gnew = self.gnum
      if name == '':
         name = str(gnew)
      gnames = self.gname
      gnames.append(name)
      newcontext = Context(gnames,self.mname)
      newcontext.name = self.name
      for g in range(self.gnum):
         newcontext.gintent[g] = self.gintent[g]
      for m in range(self.mnum):
         newcontext.mextent[m] = self.mextent[m]
      for m in range(self.mnum):
         if m in gintent: newcontext.make_incident(gnew,m)
         else: newcontext.make_nonincident(gnew,m)
      return newcontext
         
#############################################
# Manipulating context data fields directly
# may cause inconsistencies.
# Consistency can be checked. 
#############################################  
   def isconsistent(self,details=False):
      '''Context consistency check.'''
      ok = True
      good = (len(self.gname)==len(set(self.gname)))
      ok = ok and good
      if details and not good:
         print('Duplicate object names')
      good = (len(self.gintent)==self.gnum)
      ok = ok and good
      if details and (not good):
         print('Bad gintent list length')
      good = (len(self.mname)==len(set(self.mname)))
      ok = ok and good
      if details and not good:
         print('Duplicate attribute names')
      good = (len(self.mextent)==self.mnum)
      ok = ok and good
      if details and (not good):
         print('Bad mextent list length')
      for g in range(self.gnum):
         good = (type(self.gname[g])==str)
         ok = ok and good
         if details and (not good):
            print('Object '+str(g)+' has bad name type. '
                  'Must be string.')
      for g in range(self.gnum):
         good = (self.gintent[g] <= set(range(self.mnum)))
         ok = ok and good
         if details and (not good):
            print('Bad object intent '+str(g)+"' =",self.gintent[g])
      for m in range(self.mnum):
         good = (type(self.mname[m])==str)
         ok = ok and good
         if details and (not good):
            print('Attribute '+str(m)+' has bad name type. '
                         'Must be string.')
      for m in range(self.mnum):
         good = (self.mextent[m] <= set(range(self.gnum)))
         ok = ok and good
         if details and (not good):
            print('Bad attribute extent'
                  ' '+str(m)+"' =",self.mextent[m])
      for g in range(self.gnum):
         for m in range(self.mnum):
            good = ((g in self.mextent[m])==(m in self.gintent[g]))
            ok = ok and good
            if details and (not good):
               print(str(g)+' in '+str(m)+"' unequal "+str(m)+' in'
                      ' '+str(g)+"'.")
      if ok: print('Consistency check passed.')
      elif details: print('Consistency check failed.')
      else: print('Consistency check failed. '
            'Check again with "details=True".')
      return ok
#############################################        
#    Context class data field output methods
#############################################          
   def xdot_out(self,g):
      """Makes a string 'x..x.x' from object intent."""     
      outstr = ''
      for m in range(self.mnum):
         if self.isincident(g,m): outstr = outstr + 'x'
         else: outstr = outstr + '.'
      return outstr

###############################     
   def print_incidence(self):
      ''' Prints the incidence matrix without
      labels. To see more details, use print().'''
      anz = ''
      for g in range(self.gnum):
         anz = anz + '   '+ self.xdot_out(g) + '\n'
      print(anz)
          
###############################
   def gnames(self,A):
      ''' Returns a set of object names'''
      return {self.gname[g] for g in A}
     
###############################
   def mnames(self,B):
      ''' Returns a set of attribute names'''
      return {self.mname[m] for m in B}
             
###################################################
#  Formal context intent/extent methods
#  
#  make_extent(B)     
#  make_intent(A)
#  close_extent(A)
#  close_intent(B)
#
###################################################                  
   def make_extent(self,mset):
      """Computes the derivation of mset."""
      if hasattr(sys, 'ps1'):
         mset = denamed_unknown(self.mname,mset)
      extent = set(range(self.gnum))
      for m in mset:
         extent &= self.mextent[m]
      return extent
   
###############################
   def make_intent(self,gset):
      """Computes the derivation of gset."""     
      if hasattr(sys, 'ps1'):
         gset = denamed_unknown(self.gname,gset)
      intent = set(range(self.mnum))
      for g in gset:
         intent &= self.gintent[g]
      return intent
###############################
   def close_extent(self,gset):
      """Computes the closure gset'' of gset."""     
      if hasattr(sys, 'ps1'):
         gset = denamed_unknown(self.gname,gset)
      return self.make_extent(self.make_intent(gset))
   
###############################
   def close_intent(self,mset):
      """Computes closure mset''."""     
      if hasattr(sys, 'ps1'):
         mset = denamed_unknown(self.mname,mset)
      msets = self.make_extent(mset)
      closure = self.make_intent(msets)
      return closure
   
##################################################
#  Next closure algorithm
#
#  first_extent(), first_intent()
#  Both methods have optional parameters avoid and contain,
#  which by default are equal to the empty set.
#
#  next_extent(A)
#  next_intent(B)
#  number_of_concepts()
#  uplist()       list of concepts and parents
#
##################################################
   def first_extent(self, avoid = set(), contain = set()):
      ''' First extent closure.'''
      if avoid | contain == set():  
 #        self.gclosure = Closureoperator(self.gnum, self.close_extent)
         return self.close_extent(set())
      else:
 #        self.gclosure = Closureoperator(self.gnum,self.close_extent)
         return self.gclosure.first_closure(avoid, contain)

###############################
   def first_intent(self, avoid = set(), contain = set()):
      ''' First intent closure.'''
      if avoid | contain == set():  
#         self.mclosure = Closureoperator(self.mnum, self.close_intent)
         return self.close_intent(set())
      else:
#         self.mclosure = Closureoperator(self.mnum, self.close_intent)
         return self.mclosure.first_closure(avoid, contain)
   
###############################
   def next_extent(self,menge):
      return self.gclosure.next_closure(menge)
   
###############################
   def next_intent(self,menge):
      return self.mclosure.next_closure(menge)

###############################
   def number_of_concepts(self):
      '''Computes the number of intents.'''
      menge = self.first_intent()
      count = 0
      while menge is not None:
         menge = self.next_intent(menge)
         count += 1
      return count

###############################
   def uplist(self):
      ''' Gives the immutable list of all formal concepts of self
      as (extent, intent, parents), where parents is the list of
      upper neighbors. The intents are in lectic order.'''
      from copy import deepcopy
      B = self.first_intent()
      Bprime = self.make_extent(B)
      parents = []
      upl = ((deepcopy(Bprime),deepcopy(B),deepcopy(parents)),)
      count = 0
      while B is not None:
         B = self.next_intent(B)
         count += 1
         if B is not None:
            Bprime = self.make_extent(B)
            mgs = self.mungos(Bprime)
            parents = []
            for g in mgs:
               E = Bprime.copy()
               E.add(g)
               E = self.close_extent(E)
               for b in range(count):
                  if E == upl[b][0]:
                     parents = parents + [b]
                     break
            upl = upl + ((deepcopy(Bprime),deepcopy(B),deepcopy(parents)),)
      return upl

   def twenty_concepts(self,start=0):
      ul = self.uplist()
      nc = len(ul)
      k = min(nc-start,20)
      for i in range(k - 1):
         j = i + start
         print(j,': (',ul[j][0],',',ul[j][1],')')
      j = start + k - 1
      if start + 20 < nc:
         print(j,': (',ul[j][0],',',ul[j][1],')  ...')
      else: print(j,': (',ul[j][0],',',ul[j][1],') .')

   def successor_list(self,start=0):
      ul = self.uplist()
      nc = len(ul)
      k = min(nc-start,20)
      for i in range(k - 1):
         j = i + start
         print(j,': ',end='')
         un = len(ul[j][2])
         if un == 0:
            print('-- ')
         else:
            for m in range(un):
               print(ul[j][2][m],end= ' ')
            print()   
      j = start + k - 1
      print(j,end=' : ')
      if start + 20 < nc:
         for x in ul[j][2]:
            print(x,end = ' ')
         print(' ...')   
      else:
        for x in ul[j][2]:
            print(x,end = ' ')
        print(' .')

   def label_assignment(self):
      ul = self.uplist()
      for g in range(self.gnum):
         gprime = self.make_intent({g})
         for cnum in range(len(ul)):
            if ul[cnum][1]==gprime:
               print('object ',g,' : concept ',cnum)
      for m in range(self.mnum):
         mprime = self.make_extent({m})
         for cnum in range(len(ul)):
            if ul[cnum][0]==mprime:
               print('attribute ',m,' : concept ',cnum)
         
 
##################################################
#  Making a new formal context from the given one
#
#  copy()
#  dual()              shortcut: ~
#  complement()        shortcut: -
#  clarify()
#  reduce()
#  subcontext(gset,mset)
#  transitive_closure()    requires an nxn context
##################################################
   def copy(self):
      '''Makes a deep copy of a formal context.'''
      from copy import deepcopy
      return deepcopy(self)
   
###############################
   def dual(self):
      '''Returns the dual of a formal context.'''
      newcxt = Context(self.mnum,self.gnum)
      if self.name[-5:]=='_dual':
         newcxt.name = self.name[:-5]
      else: newcxt.name = self.name+'_dual'
      for g in range(self.gnum):
         newcxt.mname[g] = self.gname[g]
         newcxt.mextent[g] = self.gintent[g]
      for m in range(self.mnum):
         newcxt.gname[m] = self.mname[m]
         newcxt.gintent[m] = self.mextent[m]
      return newcxt

###  
   def __invert__(self):
      return self.dual()

###############################
   def complement(self):
      '''Makes the complementary context.'''
      newcxt = Context(self.gnum,self.mnum)
      if self.name[-5:]=='_comp':
         newcxt.name = self.name[:-5]
      else: newcxt.name = self.name+'_comp'
      for g in range(self.gnum):
         newcxt.gname[g] = self.gname[g]
         newcxt.gintent[g] = set(range(self.mnum)) - self.gintent[g]
      for m in range(self.mnum):
         newcxt.mname[m] = self.mname[m]
         newcxt.mextent[m] = set(range(self.gnum)) - self.mextent[m]
      return newcxt
   
###   
   def __neg__(self):
      return self.complement()

###############################
   def hslice(self,gset):
      '''Makes subcontext from objects in gset only.'''
      newcxt = Context(len(gset),self.mnum)
      for m in range(self.mnum):
         newcxt.mname[m] = self.mname[m]
      count = 0
      for g in gset:
         newcxt.gname[count] = self.gname[g]
         for m in range(self.mnum):
            if self.isincident(g,m):
               newcxt.make_incident(count,m)
            else: newcxt.make_nonincident(count,m)    
         count +=1
      return newcxt     

###############################
   def vslice(self,mset):
      '''Makes subcontext from attributes in mset only.'''
      newcxt = Context(self.gnum,len(mset))
      for g in range(self.gnum):
         newcxt.gname[g] = self.gname[g]
      count = 0
      for m in mset:
         newcxt.mname[count] = self.mname[m]
         for g in range(self.gnum):
            if self.isincident(g,m):
               newcxt.make_incident(g,count)
            else: newcxt.make_nonincident(g,count)    
         count +=1
      return newcxt     

###############################
   def gclarify(self):
      '''Clarifys the context's object set.'''
      cself = self.copy()
      nondeleted = set(range(self.gnum))
      for g in range(self.gnum-1):
         if g in nondeleted:  
            for h in range(g+1,self.gnum):
               if h in nondeleted:
                  if self.gintent[g]==self.gintent[h]:
                     nondeleted.remove(h)
                     cself.gname[g] = cself.gname[g]+', '+self.gname[h]
      return cself.hslice(nondeleted)
 
###############################
   def clarify(self):
      '''Clarifies the context.'''
      step = self.gclarify()
      stepp = step.dual()
      steppp = stepp.gclarify()
      return steppp.dual()

###############################
   def greduce(self):
      '''Removes reducible objects, assuming clarified.'''
      nondeleted = set(range(self.gnum))
      for g in range(self.gnum):
         huelle = set(range(self.mnum))
         if huelle == self.gintent[g]: nondeleted.remove(g)
         else:
            for h in range(self.gnum):
               if (h!=g) and self.gintent[g] < self.gintent[h]:
                  huelle = huelle & self.gintent[h]
            if self.gintent[g] == huelle:
               nondeleted.remove(g)
      return self.hslice(nondeleted)

###############################
   def reduce(self):
      '''Clarifies and reduces the context.'''
      clf = self.gclarify()
      step = clf.greduce()
      stepp = step.dual()
      clf = stepp.gclarify()
      step = clf.greduce()
      stepp = step.dual()
      adx = '-r'
      if adx == self.name[-2:]: adx = ''
      stepp.name = self.name+adx
      return stepp

###############################
   def subcontext(self,gset,mset):
      '''Returns the subcontext on (gset,mset).'''
      return (self.hslice(gset)).dual().hslice(mset).dual()

###############################
   def transitive_closure(self):
      '''
      Computes the reflexive transitive closure.
      Input instance must be a context with $|G|=|M|$.
      ''' 
      cc = self.copy()
      for k in range(self.gnum):
         cc.make_incident(k,k)
      for k in range(self.gnum):
         for i in range(self.gnum):
            if cc.isincident(i,k):
               for j in range(self.gnum):
                  if cc.isincident(k,j):
                     cc.make_incident(i,j)
      return cc

##################################################
#  Making a context from two given ones.
#
#  subposition(kk)            shortcut: /
#  apposition(kk)             shortcut: |
#  disjoint_union(kk)
#  sum(kk)                    shortcut: +
#  product(kk)                shortcut: *
#  semiproduct(kk)
#
##################################################
   def subposition(self,kk):
      '''Makes the subposition of contexts having the same attributes.'''
      if self.mnum == kk.mnum:
         ll = self.copy()   
         for g in range(kk.gnum):
            ll = ll.add_object(kk.gintent[g],name=kk.gname[g])
      ll.name = self.name + '/' + kk.name      
      return ll
# sollte man vielleicht sicherer machen (ggf. Leerzellen ergänzen)

   def __truediv__(self, ll):
      return self.subposition(ll)

###############################
   def apposition(self,kk):
      '''Makes the apposition of contexts having the same objects.'''
      result = self.dual().subposition(kk.dual()).dual()
      result.name = self.name + '|' + kk.name
      return result
   
   def __or__(self, ll):
      return self.apposition(ll)

###############################
   def disjoint_union(self,kk,disjoint=True):
      '''
      Returns the context disjoint union.
      Set optional parameter disjoint=False for proper names. 
      '''
      du = self.subposition(Context(kk.gnum,self.mnum)).apposition(
         Context(self.gnum,kk.mnum).subposition(kk))
      for g in range(self.gnum):
         if disjoint: du.gname[g] = self.gname[g]
         else: du.gname[g]='(1,' + self.gname[g] + ')'
      for g in range(kk.gnum):     
         if disjoint: du.gname[g+self.gnum] = kk.gname[g]
         else:  du.gname[g+self.gnum]='(2,' + kk.gname[g] + ')'
      for m in range(self.mnum):
         if disjoint: du.mname[m] = self.mname[m]  
         else: du.mname[m]='(1,' + self.mname[m] + ')'  
      for m in range(kk.mnum):
         if disjoint: du.mname[m+self.mnum] = kk.mname[m]  
         else: du.mname[m+self.mnum]='(2,' + kk.mname[m] + ')'
      du.name = self.name + r' $\cup$ '+ kk.name   
      return du
        
###############################
   def sum(self,kk,disjoint=True):
      '''
      Returns the context sum
      Set optional parameter disjoint=False for proper names. 
      '''
      sum = self.complement().disjoint_union(kk.complement())
      sum=sum.complement()
      sum.name= self.name + ' + ' + kk.name
      return sum

   def __add__(self, ll):
      return self.sum(ll)

###############################
   def product(self,kk):
      '''Returns the context product.'''
      gp = self.gnum * kk.gnum
      mp = self.mnum * kk.mnum        
      pp = Context(gp,mp)
      for g1 in range(self.gnum):
         for g2 in range(kk.gnum):
            g = g1 * kk.gnum + g2  
            pp.gname[g] = self.gname[g1]+'.'+kk.gname[g2]
            for m1 in range(self.mnum):
               for m2 in range(kk.mnum):
                  m = m1 * kk.mnum + m2
                  if self.isincident(g1,m1) or kk.isincident(g2,m2):
                     pp.make_incident(g,m)
      for m1 in range(self.mnum):
         for m2 in range(kk.mnum):
            m = m1 * kk.mnum + m2
            pp.mname[m] = self.mname[m1]+'.'+kk.mname[m2]
      return pp

   def __mul__(self, ll):
      return self.product(ll)

###############################
   def semiproduct(self,kk):
      '''Returns the context semiproduct.'''
      sp = Context(self.gnum * kk.gnum, self.mnum + kk.mnum)
      sp.name = self.name +' sp '+kk.name
      for m in range(self.mnum): sp.mname[m] = self.mname[m]
      for m in range(kk.mnum): sp.mname[self.mnum+m] = kk.mname[m]
      for g in range(self.gnum):
         for h in range(kk.gnum):
            gsp = g * kk.gnum + h
            sp.gname[gsp] = '('+self.gname[g]+','+kk.gname[h]+')'
            for m in range(self.mnum):
               if self.isincident(g,m): sp.make_incident(gsp,m)
         for m in range(kk.mnum):
            if kk.isincident(h,m): sp.make_incident(gsp, self.mnum+m)
      return sp
   
##################################################
#  The arrow relations, congruences and factors
#  
#  down_arrows()
#  up_arrows()
#  double_arrows()
#  perspectivities()     
#  congruences()
#  si_factor(m)    Arrow-closed subcontext   
#  is_si()         True if subdirectly irreducible
#
##################################################
   def down_arrows(self):
      ''' Returns the "downarrow"-relation in form
      of a formal context.     '''   
      da = Context(self.gname,self.mname)
      for g in range(self.gnum):
         for m in range(self.mnum):
            if not self.isincident(g,m):
               h = 0
               flag = True
               while flag and (h < self.gnum):
                  if not self.isincident(h,m):
                     if self.gintent[g] < self.gintent[h]:
                        flag = False
                  h += 1
               if flag: da.make_incident(g,m)
      return da

###############################
   def up_arrows(self):
      ''' Returns the "uparrow"-relation in form of
          a formal context. '''   
      ua = self.dual().down_arrows().dual()
      return ua

##################################################
   def double_arrows(self):
      ''' Returns the "double-arrow"-relation in form
      of a formal context.     '''   
      ba = self.empty()
      da = self.down_arrows()
      ua = self.up_arrows()
      for g in range(self.gnum):
         for m in range(self.mnum):
            if da.isincident(g,m) and ua.isincident(g,m):
               ba.make_incident(g,m)
      return ba

###############################
   def perspectivities(self):
        '''
        Returns the "double downarrows" which can be used to describe the
        congruences of a concept lattice. The congruence lattice is isomorphic
        to that of the complement of the downarrows context.
        '''
        ua = self.up_arrows()
        da = self.down_arrows()
        rel = Context(self.mnum,self.mnum)
        for g in range(self.gnum):
           for m in da.gintent[g]:
              for n in ua.gintent[g]:
                 rel.make_incident(m,n)
        rel = rel.transitive_closure()
        dda = Context(self.gnum,self.mnum)
        for g in range(self.gnum):
           for m in da.gintent[g]:
              for n in rel.mextent[m]:
                 dda.make_incident(g,n)
        return dda

###############################
   def congruences(self):
      r'''
      Returns a formal context with the property, that for each
      formal concept (A,B) the pair (G\setminus A,B) is an arrow-closed
      subcontext of self, and each such subcontext is obtained.
      '''
      return self.perspectivities().complement()
          
###############################
   def si_factor(self,m):
      '''
      The input context self should be reduced (it otherwise will be
      reduced, which might change attribute names).
      Returns a pair (H,N), where H is a subset of objects of self
      and N is a subset of attributes, such that (H,N) is the smallest
      arrow-closed subcontext of self containing m.
      '''
      cx = self.congruences()
      H = cx.make_extent({m})
      N = cx.make_intent(H)
      H = set(range(self.gnum)) - H
      return (H,N)
          
###############################
   def is_si(self):
      ''' Returns True when the concept lattice is subdirectly
      irreducible, False otherwise.'''
      cx = self.congruences()
      issi = False
      for m in range(self.mnum):
         issi = (cx.close_intent({m}) == set(range(self.mnum)))
         if issi: break
      return issi   
      
##################################################
#  Generators and such
#
#  generators_quasiorder(A)
#  mungos(A)   minimal upper neighbour generators
#  next_mingen(A)  minimal generator sets
##################################################
   def generators_quasiorder(self,A):
        '''
        Returns the quasiorder on $G$ defined by
        $$ g\\sqsubseteq h :\\iff (A\\cup\\{g\\})''\\subseteq (A\\cup\\{h\\})''.$$
        The method uses the fact that
        $$ \not\\sqsubseteq  = \bigcup_{m\\in A'} (G\\setminus m')\times m'.$$
        '''
        NQO = Context(self.gnum,self.gnum)
        NQO.gname = self.gname
        NQO.mname = self.gname
        NQO.name = 'NQO_comp'
        for m in self.make_intent(A):
           mprimecomp = set(range(self.gnum)) - self.mextent[m]
           for g in range(self.gnum):
              if g in self.mextent[m]:
                 NQO.mextent[g] = NQO.mextent[g] | mprimecomp
              else:
                 NQO.gintent[g] = NQO.gintent[g] | self.mextent[m]
        return NQO.complement()

###############################
   def mungos(self,A):
      r''' Minimal upper neighbor generator objects.
      Returns a set MG of objects such that for each upper neighbor U of A
      there is a unique g in MG for which U = (A\cup\{g\})'', and g is
      smallest with this property.
      '''
      mngs = set(range(self.gnum)) - self.close_extent(A)
      QO = self.generators_quasiorder(A)
      for g in range(self.gnum):
         if g in mngs:  
            mangos = set()
            for h in mngs:
               if QO.isincident(g,h) and (h != g): mangos.add(h)
            mngs = mngs - mangos   
            good = True
            for h in mngs:
               if (h != g) and good:  
                  if QO.isincident(h,g): good = False
            if not good: mngs.remove(g)     
      return mngs

###############################
   def number_of_maxchains(self):
      '''Computes the number of maximal chains in the concept lattice.'''
      uli = self.uplist()
      nctt = [1]                  # number of maxchains to the top element
      for c in range(1,len(uli)):
         thisnctt = 0
         for p in uli[c][2]: thisnctt += nctt[p]
         nctt = nctt + [thisnctt]
      return thisnctt
 
###############################
   def length(self):
      '''Computes the maximal length of a chain in the lattice.'''
      uli = self.uplist()
      stt = [0]                  # number of steps to the top element
      for c in range(1,len(uli)):
         thisstt = 0
         for p in uli[c][2]: thisstt = max(thisstt, stt[p])
         stt = stt + [thisstt+1]
      return thisstt+1
 
###############################
   def canonical_basis(self):
      ''' Algorithm 16 from G & O. '''
      ll = Implist(self.mname)
      ll.empcons = self.close_intent(set())
      if ll.empcons != set(): ll.addimp(Implication(set(),ll.empcons))
      A = self.close_intent(set())
      while A is not None:
         AA =  self.close_intent(A)
         if A != AA:
            DA = AA- A
            impli = Implication(A,DA)
            ll.addimp(impli)
         A = ll.next_closure(A)
      return ll
                                
###############################
   def extent_list(self):
      ''' Returns a list of extents as generated
      by next_extent'''
      global sccss
      sccss = True
      E = self.first_extent()
      lll = [E]
      while True:
         E = self.next_extent(E)
         if sccss: lll.append(E)
         else: break
      return lll

###############################
   def is_distributive(self):
      rself = self.reduce()      
      ua = rself.up_arrows()
      da = rself.down_arrows()
      dist = True
      for g in range(rself.gnum):
         if len(ua.gintent[g]) != 1:
            dist = False
         if da.gintent[g] != ua.gintent[g]:
            dist = False
         if not dist :break   
      for m in range(rself.mnum):
         if len(ua.mextent[m]) != 1:
            dist = False
         if da.mextent[m] != ua.mextent[m]:
            dist = False
         if not dist :break
      return dist   

