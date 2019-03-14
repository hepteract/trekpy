# util.py

"""Various utility functions used in this project."""

def max_elements(list1, N): 
    final_list = []

    list1 = list(list1)

    N = min(len(list1), N)
  
    for i in range(0, N):  
        max1 = 0
          
        for j in range(len(list1)):      
            if list1[j] > max1: 
                max1 = list1[j]; 
                  
        list1.remove(max1); 
        final_list.append(max1) 
          
    return tuple(final_list)
