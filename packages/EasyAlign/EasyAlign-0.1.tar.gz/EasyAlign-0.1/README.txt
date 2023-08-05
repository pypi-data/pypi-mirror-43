Thanks for using EasyAlign!

This software can align python lists of any objects that can be compared with the '==' operator (Notably, strings!)

To use it

from EasyAlign import LocalAligner
my_aligner = LocalAligner(2,-1) #2 is the match reward, and -1 is the gap penalty
seq1 = [5,4,5,1,2,3]
