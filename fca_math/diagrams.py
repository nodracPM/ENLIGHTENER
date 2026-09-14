###################################################
#
#  Python functions for making lattice diagrams
#  Output is to LaTeX or to Tkinter.
#  Input is a formal context and a placement pos.
#  which is a vector containing co-ordinates
#  of the lattice nodes, lectically ordered by 
#  intents.
#
###################################################
from fca_math.contexts import *
from fca_math.scales import *
import numpy as np
###################################################
class Placement:
   def __init__(self,length):
      self.length = length
      self.xy = np.zeros((self.length,2),dtype='float16')
      self.normalized = False     
   def __str__(self):
      return str(self.xy)

   def normalize(self):
      npos = Placement(self.length)
      npos.xy = self.xy.copy()
      if self.length > 1:
         dy = self.xy[0][1] - self.xy[self.length-1][1]
         npos.xy = [(npos.xy[i][0]/dy,npos.xy[i][1]/dy) for i in
                    range(self.length)]
         shifty = npos.xy[0][1] - 1
         shiftx = (min([p[0] for p in npos.xy]) +\
                   max([p[0] for p in npos.xy]))/2
         npos.xy = np.array([np.array([p[0]-shiftx,p[1]-shifty])\
                             for p in npos.xy])
      npos.normalized = True
      return npos
   
   def write(self,posfile):
      '''
      Writes placement to posfile.
      '''
      fname = posfile
      pos = self
      if not self.normalized:
         pos = self.normalize()
         pos.normalized = True
      if (len(fname) < 4) or (fname[0:4] != 'pos/'):
         fname = 'pos/'+fname
      if fname[-4:] != '.pos':
         fname = fname +  '.pos'
      np.savetxt(fname,pos.xy,fmt='%4.4f')

   def read(self,posfile):
      '''
      Reads placement from posfile.
      '''
      fname = posfile
      if (len(fname) < 4) or (fname[0:4] != 'pos/'):
         fname = 'pos/'+fname
      if fname[-4:] != '.pos':
         fname = fname +  '.pos'
      self.xy = np.loadtxt(fname,dtype='float')
      if abs(abs(self.xy[0][1] - self.xy[self.length-1][1])-1) > 1e-05:
         print('Not normalized.')
         self.normalized = False
      else: self.normalized = True
       
def readpos(kk,filename):
   '''
   Reads a placement for kk.
   '''
   pos = Placement(kk.number_of_concepts())
   pos.read(filename)
   return pos
      
def tkdiagram(kk,placement = None,bluenode = set(),canvas_height=500):
   '''
   Opens a tkinter window with a diagram.
   '''
   # def on_left_click(event):
   #    print(f'Mausklick bei {event.x},{event.y}')
   import tkinter as tk
   if placement is None:
      if kk.placement is None:
         print('No placement given.')
         return
      else:
         placement = kk.placement
   pos = placement      
   root = tk.Tk()
   root.title(kk.name)
   def close_window(event):
      root.destroy()
   root.bind('<Control-q>', close_window)   
#   root.bind("<Button-1>",on_left_click)
#  pos is assumed to be normalized so that the diagram is
#  centered and the height spans from 0 to 1   
   spread = canvas_height * 0.85
   hsize = max([p[0] for p in pos.xy])-min([p[0] for p in pos.xy])
   canvas_width = hsize * spread + 200
   canvas=tk.Canvas(root,width = canvas_width, height = canvas_height)
   shiftx =  0.5 * canvas_width
   shifty =  0.075 * canvas_height
   linewidth= round(1.7 + canvas_height/500)
   radius = round(5 + canvas_height/140)
   def draw_edge(i,j,shiftx,shifty,spread):
      xi = shiftx + spread * pos.xy[i][0]
      yi = shifty + spread *(1 - pos.xy[i][1])
      xj = shiftx + spread * pos.xy[j][0]
      yj = shifty + spread *(1 - pos.xy[j][1])
      canvas.create_line(xi,yi,xj,yj,width=linewidth)
   def draw_node(c,shiftx,shifty,spread):
      x = shiftx + spread * pos.xy[c][0]
      y = shifty + spread * (1 - pos.xy[c][1])
      if c in bluenode: color = 'SteelBlue1'
      else: color = 'white'
      canvas.create_oval(x-radius,y-radius,x+radius,y+radius,\
                         fill=color,width=linewidth)
      canvas.create_text(x+30,y,text=str(c))
   canvas.pack()
   ul = kk.uplist()
   for i in range(1,len(ul)):
      for on in ul[i][2]:
         draw_edge(i,on,shiftx,shifty,spread)
   for c in range(len(ul)):
      draw_node(c,shiftx,shifty,spread)                 
   root.mainloop()

def latexdiagram(kk,placement=None,diagramfilename='pydiag',bluenode=set()):
   '''
   Writes a file containing the LaTeX fca.sty text
   for a diagram of kk, given the node placements in pos.
   The nodes are in lectic order of the concept intents.
   '''
   import os
   if placement is None:
      if kk.placement is None:
         print('No placement given.')
         return
      else:
         placement = kk.placement
   pos = placement      
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
      '\\Node'+clr+' (' + str(i) + ')(' + str(12*pos.xy[i][0]) + ',' \
      + str(12*pos.xy[i][1]) + ')\n'
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
def readcsc(kk,filename='conexp.csc'):
   fname = 'csc/'+filename
   with open(fname) as cscfile:
      cscfile.readline()
      cscfile.readline()
      cscfile.readline()
      cscfile.readline()
      cscfile.readline()
      ul = kk.uplist()
      numedges=0
      cscplace=[]
      ylist = []
      for concept in range(len(ul)):
         numedges += len(ul[concept][2])
         instring = cscfile.readline()
         inlist = instring.split()
         if int(inlist[0]) != concept: print('hä? ',concept)
         point = (float(inlist[1]),float(inlist[2]))
         cscplace.append(point)
         ylist.append(float(inlist[2]))
      factor = 12/(max(ylist)-min(ylist))
      for i in range(len(ul)):
         cscplace[i] = (cscplace[i][0]*factor,cscplace[i][1]*factor)
      cscfile.readline()
      cscedge = []
      for edge in range(numedges):
         instring = cscfile.readline()
         inlist = instring.split()
         no = inlist[0][1:-1]
         nu = inlist[1][:-1]
         cscedge.append([nu,no])
      cscfile.readline()   
      cscfile.readline()   
      intentlist = [set() for concept in range(len(ul))]
      for m in range(kk.mnum):
         cnumber = int(cscfile.readline().split()[0])
         intentlist[cnumber].add(m)
      change = True
      while change:
         change = False
         for edge in cscedge:
            vu = int(edge[0])
            vo = int(edge[1])
            if not(intentlist[vo] <= intentlist[vu]):
               intentlist[vu] = intentlist[vu] | intentlist[vo]
               change = True
      mapping = [0 for c in range(len(ul))]
      for concept in range(len(ul)):
         intent = ul[concept][1]
         for i in range(len(intentlist)):
            if intent == intentlist[i]:
               mapping[concept] = i
               break
      pos = Placement(len(ul))
      for concept in range(len(ul)):
         pos.xy[concept] = cscplace[mapping[concept]]
      pos = pos.normalize()   
      return pos   
         
