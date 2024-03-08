import matplotlib.pyplot as plt
import numpy as np

import matplotlib
import matplotlib as mpl


vegetables = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21"]
farmers = ["0","1","2","3","4","5","6","7","8","9","10","11"]

harvest = np.array([[1,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11],
                    [0,1,2,3,4,5,6,7,8,9,10,11]
                    ])


fig, ax = plt.subplots()
im = ax.imshow(harvest,cmap="coolwarm",vmin=-50,vmax=20)


# Show all ticks and label them with the respective list entries
ax.set_xticks(np.arange(len(farmers)), labels=farmers)
ax.set_yticks(np.arange(len(vegetables)), labels=vegetables)



# # Rotate the tick labels and set their alignment.
# plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
#          rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(vegetables)):
    for j in range(len(farmers)):
        text = ax.text(j, i, harvest[i, j],
                       ha="center", va="center", color="w")

ax.set_title("Harvest of local farmers (in tons/year)")
fig.tight_layout(pad = 0)
plt.show()
