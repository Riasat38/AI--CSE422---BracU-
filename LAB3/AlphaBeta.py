import random
import operator

class BTNode:
  """
  as the branching factor for the game is 2. We can treat it as a Binary tree.
  """
  def __init__(self, elem):
    self.elem = elem
    self.right = None
    self.left = None

def get_tree_depth(node):

    if node is None:
        return 0  
    else:
        left_depth = get_tree_depth(node.left)
        right_depth = get_tree_depth(node.right)
        return max(left_depth, right_depth) + 1

def isleaf(node):
   if node.right == None and node.left == None:
      return True
   else:
      return False
       
def inorder(root):
  if root == None:
    return
  inorder(root.left)
  print(root.elem, end = ' ')
  inorder(root.right)

def tree_construction(arr, i = 1):
  if i>=len(arr) or arr[i] == None:
    return None
  p = BTNode(arr[i])
  p.left = tree_construction(arr, 2*i)
  p.right = tree_construction(arr, 2*i+1)
  return p

def build_gameTree(depth: int,leaf_nodes: list,pac_man = False):
    nodes = (2**(depth+1)) - 1   # Total number of nodes
    arr = [None]                 # 1based indexing for easy tree_construction
    # internal nodes
    for _ in range(1, (2**depth)):  # Until the last level
        arr.append(0)
    # leaf nodes
    i = 0
    for _ in range((2**depth), (2**(depth+1))):  
        if pac_man:
           arr.append(leaf_nodes[i])
           i+=1
        else:
           arr.append(random.choice(leaf_nodes))
    return tree_construction(arr)

#algorithm
def MiniMax(depth,tree,ismax: bool, pac_man:bool = False):
   #inorder(tree)
   #leaf node
   if isleaf(tree):
      return tree

   if pac_man:
      left = MiniMax(depth + 1, tree.left, True,pac_man=True)
      right = MiniMax(depth + 1, tree.right, True,pac_man=True)
      tree.elem = max(left.elem,right.elem)
      
   else:
      if ismax:
         left = MiniMax(depth + 1, tree.left, False)
         right = MiniMax(depth + 1, tree.right, False)
         tree.elem = max(left.elem,right.elem)
      else:
         left = MiniMax(depth + 1, tree.left, True)
         right = MiniMax(depth + 1, tree.right, True)
         tree.elem = min(left.elem,right.elem)
           
   #print(tree.elem)
   return tree

def AlphaBetaPruning(depth, tree, alpha, beta, ismax):

    if isleaf(tree):
       return tree 

    if ismax:  
        left = AlphaBetaPruning(depth + 1, tree.left, alpha, beta, False)
        right = AlphaBetaPruning(depth + 1, tree.right, alpha, beta, False)

        if left:
            alpha = max(alpha,left.elem)
        if right:
            alpha = max(alpha, right.elem)

        tree.elem = alpha
        if alpha >= beta:  
            return tree
    else:  # Minimizer's turn
        left = AlphaBetaPruning(depth + 1, tree.left, alpha, beta, True)
        right = AlphaBetaPruning(depth + 1, tree.right, alpha, beta, True)

        if left:
            beta = min(beta, left.elem)
        if right:

            beta = min(beta, right.elem)

        tree.elem = beta
        if alpha >= beta:  # Alpha cutoff
            return tree

    return tree

def pacman_game(c: int):

   max_depth = 3 
   leaf_nodes = [3, 6, 2, 3, 7, 1, 2, 0]     #this is not chosen randomly but chronologically assigned from left to right
   game_tree = build_gameTree(max_depth,leaf_nodes,pac_man=True)
   game_tree2 = build_gameTree(max_depth,leaf_nodes,pac_man=True)
   game_tree3 = build_gameTree(max_depth,leaf_nodes,pac_man=True)
   
   game_score = MiniMax(0,game_tree,True).elem
   #print(game_score)
   power_used_score = (MiniMax(0,game_tree2,True,pac_man=True)).elem - c
   #print(power_used_score)
   alphabeta_score = AlphaBetaPruning(0,game_tree3,float('-inf'), float('inf'), True).elem
   #print(alphabeta_score)

   strategy = ""
   if game_score > power_used_score:
      strategy += "Do not use power!!"
   else:
      strategy += "Use power!!"

   if alphabeta_score > power_used_score:
      strategy += "Using Power is Not Beneficial!"
   else:
      strategy += "Using power is Beneficial"

   print(strategy) 
  


if __name__ == '__main__':
    try:
       print("====Mortal Kombat====")
       player_turn = int(input("Scorpion(0) || Sub-Zero(1) :"))
       assert player_turn in [0,1]
       player = { 0:"Scorpion", 1:"Sub-Zero"}
       score_tab = [0,0]
       depth = 0
       max_depth = 5
       
       for i in range(3): #3 rounds
            game_tree = build_gameTree(max_depth,[1,-1]) #possible moves in each turn for the player
            print(f"Round{i+1},Fight!")
            score = MiniMax(depth,game_tree,True).elem
            #print(score)
            if  score == 1: #maximizer wins
               winner = score and player_turn
            else:          #minimizer wins
               winner = operator.xor(1,player_turn)            
            score_tab[winner] +=1
            #print(score_tab)
            print(f"Round{i+1} winner: {player[winner]}")  
            player_turn = operator.xor(1,player_turn) 

       game_winner = player[score_tab.index(max(score_tab))]
       print(f"Game Winner: {game_winner}")


       print("==++==PACMAN==++==")
       c = int(input("Choose between 2/5 to use power:"))
       assert c in [2,5]
       pacman_game(c)
    except AssertionError:
       print("Your Entered Value is Invalid for this case")
      
           
        
       