###################################################
#
#  Python functions for making lattice diagrams
#  Output is to LaTeX.
#  Input is a formal context and a placement,
#  which is a vector pos, containing co-ordinates
#  of the lattice nodes, lectically ordered by 
#  intents.
#
###################################################
from fca_math.contexts import *
###################################################
def latexdiagram(kk,pos,diagramfilename='pydiag',bluenode={}):
   '''
   Writes a file containing the LaTeX fca.sty text
   for a diagram of kk, given the node placements in pos.
   The nodes are in lectic order of the concept intents.
   '''
   import os
   workingdir = os.getcwd()
   latexdir = workingdir+'/latex'
   os.chdir(latexdir)
   if (len(diagramfilename) < 5) or \
      (diagramfilename[-4:] !=  '.tex'):
      diagramfilename += '.tex'
   outtext = '\\documentclass{article}\n\\usepackage{tikz}\n'+\
   '\\usetikzlibrary{fca}\n\\begin{document}\n'+\
   '\\begin{tikzpicture}\n\\begin{diagram}'+\
   '\\fcaCircleSize{.4}\n'
   ul = kk.uplist()
   for i in range(len(ul)):
      clr = ''
      if i in bluenode: clr='[fill=blue]'
      outtext = outtext + \
      '\\Node'+clr+' (' + str(i) + ')(' + str(pos[i][0]) + ',' \
      + str(pos[i][1]) + ')\n'
   for i in range(1,len(ul)):
      for on in ul[i][2]:
         outtext = outtext + '\\Edge(' + str(i) + ')(' + str(on) + ')\n'
   outtext = outtext + \
   '\\end{diagram}\n\\end{tikzpicture}\n\\end{document}\n'      
   with open(diagramfilename,'w') as f:
      f.write(outtext)
      f.close()
   os.system("pdflatex %s" % diagramfilename)
   pdffilename = diagramfilename[:-3] + 'pdf'
   os.system("okular %s" % pdffilename)
   os.chdir(workingdir)
                                          
#############################################
def read_rowwise_pos(kk,filename):
   '''
   Reads a pos-file in which the co-ordinates are
   given row-wise.
   '''
   kknc = kk.number_of_concepts()
   posfile = open('pos/'+filename,'r')
   pos = [(0.,0.) for j in range(kknc)]
   count = 0   
   for line in posfile:
      inpair = line.split()
      pos[count] = (float(inpair[0]),float(inpair[1]))
      count +=1
      if count  > kknc: break
   posfile.close()   
   return pos   

# #############################################                    
# def readpos(posfile):
#    '''
#    Reads placement co-ordinates from a .pos - file.
#    '''
#    fname = posfile
#    if (len(fname) < 4) or (fname[0:4] != 'pos/'):
#       fname = 'pos/'+fname
#    if fname[-4:] != '.pos':
#       fname = fname +  '.pos'
#    with open(fname,'r') as posfile:
#       for line in posfile:
#          input = line
#          break
#    inlist = input.split(sep = ')')
#    pos = []
#    ly = []
#    for i in range(len(inlist)-1):
#       entry = inlist[i].split(sep='(')[1].split(sep=',')
#       posx = float(entry[0])
#       posy = float(entry[1])
#       pos.append((posx,posy))
#       ly.append(posy)
#    factor = 12/(max(ly) - min(ly))
#    for i in range(len(ly)):
#       pos[i] = (pos[i][0]*factor,pos[i][1]*factor)
#    return pos
#############################################                    
def readpos(posfile):
   '''
   Reads placement co-ordinates from a .pos - file.
   '''
   fname = posfile
   if (len(fname) < 4) or (fname[0:4] != 'pos/'):
      fname = 'pos/'+fname
   if fname[-4:] != '.pos':
      fname = fname +  '.pos'
   coords = []   
   try:
      with open(fname,'r') as posfile:
         for line in posfile:
            parts = line.split()
            if len(parts) == 2:
               pair = (float(parts[0]), float(parts[1]))
               coords.append(pair)
   except FileNotFoundError:
      print('No such file')
   except ValueError:
      print('Error: malformed data.')
   return coords


