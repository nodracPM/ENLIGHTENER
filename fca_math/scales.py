##############################################
# Scales are contexts with a special role.
# Here they are introduced separately for clarity
##############################################
from fca_math.contexts import *
from fca_math.diagrams import *
##############################################
#  class Scale: predefined formal contexts 
##############################################
class Scale(Context):
   pass
##############################################
#
#  The definitions below are for
#
#  Scale.nominal(n)
#  Scale.contranominal(n)
#  Scale.ordinal(n)
#  Scale.reverse_ordinal(n)
#  Scale.interordinal(n)
#  Scale.integer_partitions(n)
#  Scale.set_partitions(n)
#  Scale.tamari(n)
#  Scale.noncrossing(n)
#  Scale.permutations(n)
#  Scale.pg2(d)
#  Scale.dichotomic()        # 2 x 2 context
#  Scale.biordinal(n,m)
#
#  Further definitions require as input argument
#  a relation rel, in form of an nxn context:
#
#  Scale.contraordinal(rel)
#  Scale.general_ordinal(rel)
#  Scale.max_antichains(rel)
#  Scale.general_interordinal(rel)
#  Scale.convex_ordinal(rel)
#
##############################################
   @classmethod
   def nominal(cls,n):
      '''Returns the nominal scale for n.''' 
      nn = Context(n,n)
      nn.name = r'$\mathbb{N}_{'+str(n)+'}$'
      for i in range(n):
         nn.gname[i] = str(i+1)
         nn.mname[i] = str(i+1)
         nn.make_incident(i,i)
      pos = Placement(n+2)   
      pos.xy = np.array([[0,2]]+[[-(n-1)/4+i/2,1] for i in range(n)]+[[0,0]])   
      nn.placement = pos.normalize()
      return nn     

##############################################
   @classmethod
   def contranominal(cls,n):
      '''Returns the contranominal scale for n.''' 
      from fca_math.aldi import setrepmatrix, srm_evaluate
      cn = cls.nominal(n).complement()
      cn.name = r'$\mathbb{N}_{'+str(n)+'}^c$'
      noc = 2**n
      pos = Placement(noc)
      vec = np.array([[0,0] for i in range(n)]
                      +[[2**i-2**(n-i-1),2**i+2**(n-i-1)] for i in range(n)])
      srm = setrepmatrix(cn)
      pos = srm_evaluate(cn,srm,vec)
      cn.placement = pos
      return cn
   
###############################
   @classmethod
   def ordinal(cls,n):
      '''Returns the ordinal scale for n.'''
      os = Context(n,n)
      os.name = r'$\mathbb{O}_'+str(n)+'$'
      for g in range(n):
         os.gname[g] = str(g+1)
         os.mname[g] = r'$\leq '+str(g+1)+'$'
         for m in range(n):
            if g <= m: os.make_incident(g,m)
      return os
   
###############################
   @classmethod
   def reverse_ordinal(cls,n):
      '''Returns the reverse ordinal scale for n.'''
      osc = Context(n,n)
      for g in range(n):
         osc.gname[g] = str(g+1)
         osc.mname[g] = r'$\geq '+str(g+1)+'$'
         for m in range(n):
            if g >= m: osc.make_incident(g,m)
      return osc
   
###############################
   @classmethod
   def interordinal(cls,n):
      '''Returns the interordinal scale for n.'''
      from fca_math.aldi import setrepmatrix, srm_evaluate
      iosc = Scale.ordinal(n).apposition(Scale.reverse_ordinal(n))
      iosc.name = r'$\mathbb{I}_'+str(n)+'$'
      kk = iosc.reduce()
      srm = setrepmatrix(kk)      
      vec = np.array([[0,0] for g in range(n)]+[[1,1] for m in range(n-1)]
                     + [[-1,1] for m in range(n-1)])
      pos = Placement(len(srm))
      pos = srm_evaluate(kk,srm,vec)
      iosc.placement = pos
      return iosc
    
###############################
   @classmethod
   def integer_partitions(cls,n):
      ''' Context for the lattice of integer partitions'''  
      nn = ((n+1)*(n+2))//6 -1
      ip = Context(nn,nn)
      count = 0
      pg = [[]]*nn
      pm = [[]]*nn
      for a in range(n+1):
         for m in range(1,(n // 2) + 1):
            q = (n-a) // m
            r = (n-a) %  m
            if (m > r) and (q >= 2) and ((a == 0) or (r == 0) or (q > 2)):
               pg[count] = []
               for s in range(r):
                  pg[count].append(q+1)
               for s in range(m-r):
                  pg[count].append(q)
               for s in range(a):
                  pg[count].append(1)
               ip.gname[count] = str(pg[count])
               count += 1
      for g in range(nn):
         pm[g] = []
         for i in range(n):
            j = 0
            for k in pg[g]:
               if k > i: j += 1
            if j == 0: break    
            else: pm[g].append(j)
         ip.mname[g] = str(pm[g])
      for g in range(nn):
         for m in range(nn):
            sumg = 0
            summ = 0
            incident = True
            for i in range(n):                  
               if i < len(pg[g]): sumg += pg[g][i]
               if i < len(pm[m]): summ += pm[m][i]
               if sumg > summ:
                  incident = False
                  break
            if incident: ip.make_incident(g,m)   
      return ip         

###############################
   @classmethod
   def tamari(cls,n):
      ''' Context for the Tamari lattice '''
      nc2 = (n*(n-1))//2
      tc = Context(nc2,nc2)
      tc.name = 'Tamari('+str(n)+')'
      ilist = [None] * nc2
      jlist = [None] * nc2
      gcount = 0
      for j in range(1,n+1):
         for i in reversed(range(1,j)):
            ilist[gcount] = i  
            jlist[gcount] = j  
            tc.gname[gcount] = str(i)+'|'+str(j)
            tc.mname[gcount] = str(i)+'|'+str(j)
            gcount +=1
      for g in range(nc2):
         for m in range(nc2):
            if not ((ilist[m] <= ilist[g]) and (ilist[g] < jlist[m]) \
                    and (jlist[m] <= jlist[g])):
               tc.make_incident(g,m)
      return tc           
                                
###############################
   @classmethod
   def set_partitions(cls,n):
      ''' Context for the partition lattice '''
      sccss = True
      gn = n * (n - 1) // 2
      mn = 2**(n-1)
      sp = Context(gn,mn)
      cn = Scale.contranominal(n-1)
      count = 0
      for i in range(1,n):
         for j in range(i):
            sp.gname[count] = str({i,j})
            count += 1
      count = 0
      A = cn.first_extent()
      sp.mname[count] = str({})
      while sccss:
         A = cn.next_extent(A)
         sccss = (A is not None)
         count += 1
         if sccss: sp.mname[count] = str(A)
      sccss = True   
      countm = 0
      A = cn.first_extent()
      while sccss:
         countg = 0
         for i in range(1,n):
            for j in range(i):
               if len(A & {i,j}) != 1: sp.make_incident(countg,countm)
               countg += 1
         countm += 1
         A = cn.next_extent(A)
         sccss = (A is not None)
      return sp   
                                
###############################
   @classmethod
   def noncrossing(cls,n):
      ''' Context for the lattice of non-crossing partitions '''
      gn = n * (n-1) // 2
      nc = Context(gn,gn)
      count = 0
      for i in range(1,n):
         for j in range(i):
            nc.gname[count] = str({j,i})
            nc.mname[count] = str({j,i})
            count += 1
      countg = 0      
      for jg in range(1,n):
         for ig in range(jg):
            countm = 0
            for jm in range(1,n):
               for im in range(jm):
                  if not ((ig < im) and (im <= jg) and (jg < jm)) and\
                     not ((im <= ig) and (ig < jm) and (jm <= jg)):
                     nc.make_incident(countg,countm)
                  countm += 1
            countg += 1
      return nc      
                     
###############################
   @classmethod
   def permutations(cls,n):
      nn = 2**n -n -1
      pp = Context(nn,nn)
      cn = Scale.contranominal(n)
      E = cn.first_extent()
      count = 0
      while E is not None:
         E = cn.next_extent(E)
         if E is None: break
         if E != set(range(len(E))):
            gw = ''
            mw = ''
            for i in E:
               gw = gw + chr(48 + i)
               mw = mw + chr(47 + n - i)
            F = set(range(n)) - E   
            for j in F:
               gw = gw + chr(48 + j)
               mw = mw + chr(47 + n - j)
            pp.gname[count] = gw
            pp.mname[count] = mw
            count += 1
      for g in range(nn):
         invg = inversions(pp.gname[g])
         for m in range(nn):
            invm = inversions(pp.mname[m])
            if invg <= invm: pp.make_incident(g,m)
      return pp
   
###############################
   @classmethod
   def additively_saturated(cls,n):
      il = Implist.make_addsat(n)
      clo = Closureoperator.from_implist(il)
      return clo.make_context()
   
###############################
   @classmethod
   def pg2(self,d):
      ''' Returns the formal context for the projective geometry of
      dimension d-1 over GF(2), i.e., of the lattice of subvectorspaces
      of GF(2)**{d}'''
      zweid = 2**d
      pg = Context(zweid,zweid)
      pg.name = 'PG(2,'+str(d-1)+')'
      for i in range(zweid):        
         name = str(bin(zweid+i))[3:]
         pg.gname[i] = name
         pg.mname[i] = name
         v1 = list(bin(zweid+i))[3:]
         for j in range(zweid):
            v2 = list(bin(zweid+j))[3:]
            sp = 0
            for k in range(d):
               sp = sp + int(v1[k])*int(v2[k])
            sp = sp % 2
            if sp == 0: pg.make_incident(i,j)
      return pg         
                                
###############################
   @classmethod
   def dichotomic(cls):
      '''Returns the dichotomic scale.'''
      dd = Scale.nominal(2)
      dd.name = r'$\mathbb{D}$'
      dd.gname[0] = str(0)
      dd.gname[1] = str(1)
      dd.mname[0] = str(0)
      dd.mname[1] = str(1)
      return dd
    
###############################
   @classmethod
   def biordinal(cls,n1,n2):
      '''Returns the biordinal scale.'''
      bio = Scale.ordinal(n1).disjoint_union(Scale.reverse_ordinal(n2))
      bio.name = r'$\mathbb{M}_{'+str(n1)+','+str(n2)+'}$'
      for g in range(n1,n1 + n2):
         bio.gname[g] = str(g + 1)
         bio.mname[g] = r'$\geq ' + str(g + 1) + '$'
      return bio
    
###############################
   @classmethod
   def contraordinal(cls,rel):
      '''
      Returns the contra(quasi-)ordinal scale for the
      quasi-order generated by \texttt{rel}, which should be
      a relation.
      '''
      return rel.transitive_closure().complement().dual()

###############################
   @classmethod
   def general_ordinal(cls,rel):
      '''
      Returns the general ordinal scale for the
      quasi-order generated by \texttt{rel}, which should be
      a relation.
      '''
#      return rel.transitive_closure().complement().dual()

###############################
   @classmethod
   def max_antichains(cls,rel):
      '''
      Returns the scale for the lattice of maximal antichains of
      the quasi-order generated by \texttt{rel}, which should be
      a relation.
      '''
      tc = rel.transitive_closure()
      for g in range(rel.gnum):
         tc.make_nonincident(g,g)
      return tc.complement().dual()

###############################
   @classmethod
   def general_interordinal(cls,rel):
      '''
      Returns the general interordinal scale for a given
      (quasi-) order generated by \texttt{rel}.
      The latter must be a relation.
      '''
      order = rel.transitive_closure()
      firsthalf = order.copy()
      secondhalf= order.dual()
      for m in range(order.mnum):
         firsthalf.mname[m]  = r'\leq '+order.mname[m]
         secondhalf.mname[m] = r'\geq '+order.mname[m]
      result = firsthalf.apposition(secondhalf)
      result.name = 'Interordinal'
      return result
   
###############################
   @classmethod
   def convex_ordinal(cls,rel):
      '''
      Returns the convex-ordinal scale for a given
      (quasi-) order generated by \texttt{rel}.
      The latter must be a relation.
      '''
      cosc = Scale.contraordinal(rel)
      cosd = cosc.dual()
      for m in range(cosc.mnum):
         cosc.mname[m] = '\\ngeq ' + cosc.mname[m]     
         cosd.mname[m] = '\\nleq ' + cosd.mname[m]     
      result = cosc.apposition(cosd)
      result.name = 'Convex-ordinal'
      return result

###############################
   
   
