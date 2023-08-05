#Programming was done by James Conley at 2am on a Monday
#Hopefully others will get some use out of it too :)
#If you find any bugs or want to say hi you can find me at github.com/JamesDConley
class LocalAligner: #This is the Smith-Waterman Algorithm
    def __init__(self,  match_reward,  gap_penalty):
        self.match_reward = match_reward
        self.gap_penalty = gap_penalty
    def score(self,  i,  j,  seq1,  seq2):
        if seq1[i] == seq2[j]:
            return self.match_reward
        else:
            return 0
    def traceback(self, max_i,  max_j):
         seq1 = self.seq1
         seq2 = self.seq2
         directions_table = self.directions_table
         current = directions_table[max_i][max_j]
         current_i = max_i
         current_j = max_j
         aligned_seq1 = []
         aligned_seq2 = []
         while current != 3:
             if current == 0:
                aligned_seq1.append( seq1[current_i-1])
                aligned_seq2.append( seq2[current_j-1])
                current_i-=1
                current_j-=1
             elif current == 1:
                aligned_seq1.append( seq1[current_i-1])
                aligned_seq2.append('-')
                current_i-=1
             elif current == 2:
                aligned_seq1.append('-')
                aligned_seq2.append(seq2[current_j-1])
                current_j-=1
             current = directions_table[current_i][current_j]
         aligned_seq1.reverse()
         aligned_seq2.reverse()
         return aligned_seq1,  aligned_seq2
    def align(self,  seq1,  seq2):
        self.seq1 = seq1
        self.seq2 = seq2
        #Friendly reminder that len of a list in python is constant time
        max = 0 #This is for keeping track of the maximum value entry so we don't have to search again later
        max_i = 0
        max_j = 0
        table = []
        directions_table = []
        for i in range(len(seq1) + 1):
            table.append((len(seq2)+1)*[0])
            directions_table.append((len(seq2)+1)*[3])
        for i in range(1, len(seq1)+1): #'i' will index sequence 1
            for j in range(1, len(seq2)+1): #'j' will index sequence 2
                options = [table[i-1][j-1] + self.score(i-1, j-1, seq1, seq2),  table[i-1][j] + self.gap_penalty,  table[i][j-1] + self.gap_penalty,  0]
                max_val = 0
                max_index = 3
                for k in range(len(options)-1):
                    if options[k] > max_val:
                        max_index = k
                        max_val = options[k]
                directions_table[i][j] = max_index
                table[i][j] = max_val
                if table[i][j] > max:
                    max = table[i][j]
                    max_i = i
                    max_j = j
        self.table = table
        self.directions_table = directions_table
        seq1,  seq2 = self.traceback(max_i, max_j)
        return seq1,  seq2, max
        
class GlobalAligner:    #This is the Needleman–Wunsch Algorithm
    def __init__(self,  match_reward,  gap_penalty):
        self.match_reward = match_reward
        self.gap_penalty = gap_penalty
    def score(self,  i,  j,  seq1,  seq2):
        if seq1[i] == seq2[j]:
            return self.match_reward
        else:
            return 0
    def traceback(self, max_i,  max_j):
         seq1 = self.seq1
         seq2 = self.seq2
         directions_table = self.directions_table
         current = directions_table[max_i][max_j]
         current_i = max_i
         current_j = max_j
         aligned_seq1 = []
         aligned_seq2 = []
         while current != 3:
             if current == 0:
                aligned_seq1.append( seq1[current_i-1])
                aligned_seq2.append( seq2[current_j-1])
                current_i-=1
                current_j-=1
             elif current == 1:
                aligned_seq1.append( seq1[current_i-1])
                aligned_seq2.append('-')
                current_i-=1
             elif current == 2:
                aligned_seq1.append('-')
                aligned_seq2.append(seq2[current_j-1])
                current_j-=1
             current = directions_table[current_i][current_j]
         aligned_seq1.reverse()
         aligned_seq2.reverse()
         return aligned_seq1,  aligned_seq2
    def align(self,  seq1,  seq2):
        self.seq1 = seq1
        self.seq2 = seq2
        #Friendly reminder that len of a list in python is constant time
        table = []
        directions_table = []
        for i in range(len(seq1) + 1):
            table.append((len(seq2)+1)*[0])
            directions_table.append((len(seq2)+1)*[3])
        for i in range(1, len(seq1)+1):
            table[i][0] = self.gap_penalty*i
            directions_table[i][0] = 1
        for i in range(1, len(seq2)+1):
            table[0][i] = self.gap_penalty*i
            directions_table[0][i] = 2
        for i in range(1, len(seq1)+1): #'i' will index sequence 1
            for j in range(1, len(seq2)+1): #'j' will index sequence 2
                options = [table[i-1][j-1] + self.score(i-1, j-1, seq1, seq2),  table[i-1][j] + self.gap_penalty,  table[i][j-1] + self.gap_penalty]
                max_val = options[0]
                max_index = 0
                for k in range(1, len(options)):
                    if options[k] > max_val:
                        max_index = k
                        max_val = options[k]
                directions_table[i][j] = max_index
                table[i][j] = max_val
        self.table = table
        self.directions_table = directions_table
        score =  table[len(seq1)][len(seq2)]
        seq1,  seq2 = self.traceback(len(seq1), len(seq2))
        return seq1,  seq2, score
