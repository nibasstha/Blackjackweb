import matplotlib.pyplot as plt
import numpy as np

import matplotlib
import matplotlib as mpl

table = np.load('same_value_hands_table_v4.npy',allow_pickle=True)

action_idx_to_action = {
  0:"stand",
  1:'hit',
  2:'double',
  3:"split"
}

true_count_zero = []
true_count_positive = []
true_count_negative = []

for i in range(10):
  zero_action_array=[]
  positive_action_array=[]
  negative_action_array=[]

  print("-----------------------")
  for j in range(11):
    zero = table[i,j,0].argmax()
    positive = table[i,j,1].argmax()
    negative = table[i,j,2].argmax()


    print(table[i,j,0])

  

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

ax.set_title("Heatmap for same value hands when true_count_zero")
fig.tight_layout(pad = 0)
plt.show()




  
