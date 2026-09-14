###################################################
#
#  fca_math/carrier.py contains tools to
#  switch between the names of elements and
#  their indices in the carrier list.
#
###################################################

import ast

def setinput(whatever):
   """
   Converts input to a set. Supports:
   - Existing sets
   - Strings representing sets (e.g., '{1, 2, 3}')
   - 'x.x' strings where x/X indices become set elements
   - Empty strings/dicts -> empty set
   """
   # 1. If it's already a set, we're done
   if isinstance(whatever, set):
      return whatever

   # 2. Handle empty cases (None, '', [], {})
   if not whatever: 
      return set()

   # 3. Handle string inputs
   if isinstance(whatever, str):
      whatever = whatever.strip()
      if whatever.startswith('{') and whatever.endswith('}'):
         try:
            result = ast.literal_eval(whatever)
            return set(result) if isinstance(result, (set, list, tuple)) else set()
         except (ValueError, SyntaxError):
            return set()
      
      # Handle the 'x.x.x' bitmask logic using a set comprehension
      return {i for i, char in enumerate(whatever) if char in 'xX'}

   # 4. Fallback for other iterables or return empty set if not iterable
   try:
      return set(whatever)
   except TypeError:
      return set()

def set_carrier(carrier):
   '''
   The base set (= carrier) may be specified either as a number,
   in which case it is replaced by a list ['0','1',..], or as a list.
   '''
   if isinstance(carrier, int):
      # Ensure size isn't negative for range
      size = max(0, carrier)
      carrier = [str(i) for i in range(size)]
   else:
      # Assuming carrier is a list or other iterable
      size = len(carrier)
      
   return carrier, size

def named_set(carrier, nset):
   ''' Replace indices by element names '''
   return {carrier[i] for i in nset}

def denamed_set(carrier, nset):
   ''' Replace element names by indices. '''
   # Using a set for nset lookup is O(1) instead of O(n)
   lookup = set(nset)
   return {i for i, val in enumerate(carrier) if val in lookup}

def denamed_unknown(carrier, whatever):
   '''
   Replace input of unknown form by indices. Input may be a set of indices,
   or a set of names, or an xdot word.
   '''
   # 1. Handle non-set inputs (Strings or Empty values)
   if not isinstance(whatever, set):
      if not whatever: # Catches '', {}, None, etc.
         return set()
      
      if isinstance(whatever, str):
         whatever = whatever.strip()
         if whatever.startswith('{'):
            try:
               whatever = set(ast.literal_eval(whatever))
            except (ValueError, SyntaxError):
               return set()
         else:   
            # xdot word logic (indices of x/X)
            return {i for i, c in enumerate(whatever) if c in 'xX'}
   
   # 2. If it is a set, check if it contains names (strings) or indices
   if whatever:
      # Get an arbitrary element to check type without a full loop
      first_elem = next(iter(whatever))
      if isinstance(first_elem, str):
         return denamed_set(carrier, whatever)
         
   return whatever
