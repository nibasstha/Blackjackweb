import numpy as np

normal_hands_table = np.load('normal_hands_table.npy',allow_pickle=True)
usable_ace_hands_table = np.load('usable_ace_hands_table.npy',allow_pickle=True)
same_value_hands_table = np.load('same_value_hands_table.npy',allow_pickle=True)



def main():
  print(usable_ace_hands_table[1])


if __name__ == '__main__':
  main()