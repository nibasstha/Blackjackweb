import matplotlib.pyplot as plt
import numpy as np

import matplotlib
import matplotlib as mpl

normal_hands_table = np.load('usable_ace_hands_table_v4.npy',allow_pickle=True)

action_idx_to_action = {
  0:"hit",
  1:'stand',
  2:'double',
  3:"split"
}

true_count_zero = []
true_count_positive = []
true_count_negative = []

play_idx = 0 # 0 for double valid table, 1 for double invalid table

for i in range(10):
  zero_action_array=[]
  positive_action_array=[]
  negative_action_array=[]

  for j in range(11):
    print(normal_hands_table[i,j,0,play_idx])

    if play_idx == 0:
      zero = normal_hands_table[i,j,0,play_idx].argmax()
      positive = normal_hands_table[i,j,1,play_idx].argmax()
      negative = normal_hands_table[i,j,2,play_idx].argmax()
    else:
      if normal_hands_table[i,j,0,play_idx,0] > normal_hands_table[i,j,0,play_idx,1]:
        zero = 0
      elif normal_hands_table[i,j,0,play_idx,0] == normal_hands_table[i,j,0,play_idx,1]:
        zero = 8
      else:
        zero = 1

      if normal_hands_table[i,j,1,play_idx,0] > normal_hands_table[i,j,1,play_idx,1]:
        positive = 0
      elif normal_hands_table[i,j,1,play_idx,0] == normal_hands_table[i,j,1,play_idx,1]:
        positive = 8
      else:
        positive = 1
      
      if normal_hands_table[i,j,2,play_idx,0] > normal_hands_table[i,j,2,play_idx,1]:
        negative = 0
      elif normal_hands_table[i,j,2,play_idx,0] == normal_hands_table[i,j,2,play_idx,1]:
        negative = 8
      else:
        negative = 1
   

    # zero_action = action_idx_to_action[zero]
    # zero_action_array.append(zero_action)
    zero_action_array.append(zero)

    # positive_action = action_idx_to_action[positive]
    # positive_action_array.append(positive_action)
    positive_action_array.append(positive)

    # negative_action = action_idx_to_action[negative]
    # negative_action_array.append(negative_action)
    negative_action_array.append(negative)

  true_count_zero.append(zero_action_array)
  true_count_negative.append(negative_action_array)
  true_count_positive.append(positive_action_array)


player_sum = ["1","2","3","4","5","6","7","8","9","10"]
dealer_sum = ["1","2","3","4","5","6","7","8","9","10","11"]

heat_map_true_count_zero = np.array(true_count_zero)
heat_map_true_count_positive = np.array(true_count_positive)
heat_map_true_count_negative = np.array(true_count_negative)

fig,ax = plt.subplots()
im = ax.imshow(heat_map_true_count_zero,cmap="coolwarm",vmin=-50,vmax=20)

ax.set_xticks(np.arange(len(dealer_sum)), labels=dealer_sum)
ax.set_yticks(np.arange(len(player_sum)), labels=player_sum)

for i in range(len(player_sum)):
    for j in range(len(dealer_sum)):
        text = ax.text(j, i, heat_map_true_count_zero[i, j],
                       ha="center", va="center", color="w")

ax.set_title("Heatmap for usable ace hands when true count is zero , double is valid")
fig.tight_layout(pad = 0)
plt.show()




  
