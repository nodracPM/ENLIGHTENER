def bond_implist(kk1,kk2):
   bcarrier=[(g,m) for g in range(kk1.gnum) for m in range(kk2.mnum)]
   bilist = Implist(bcarrier)
   il1 = kk1.dual.canonical_basis()
   for imp in il1.imp:
      for m in range(kk2.mnum):
         Pm = {(g,m) for g in imp.premise}
         Cm = {(g,m) for g in imp.conclusion}
         bilist.addpc(Pm,Cm)
   for imp in kk2.canonical_basis():
      for g in range(kk1,mnum):
         Pg = {(g,m) for m in imp.premise}
         Cg = {(g,m) for m in imp.conclusion}
         bilist.addpc(Pg,Cg)
   return bilist

   
