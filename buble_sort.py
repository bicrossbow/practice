from __future__ import print_function
import time
import random

def bubble_sort(list):
    sz = len(list)
    count_swap = 0
    need_swap = True
    print(list)
    while need_swap:
        for i in range(0,sz-1):
            #stop condition
            if i == sz-2:
                if list[i] > list[i+1]:
                    print('end of list, start over')
                    pass
                else:
                    print('sort done')
                    need_swap = False

            # swap condition 
            if list[i] > list[i+1]:
                temp = list[i+1]
                list[i+1] = list[i]
                list[i] = temp
                count_swap = count_swap + 1
                print(count_swap, list)


if __name__ == '__main__':
    sz = 10
    list = range(0,sz-1)
    for i in range(0,sz-1):
        list[i]=random.randint(0,100)

    list_copy = list

    start_time = time.time()
    bubble_sort(list_copy)
    end_time = time.time()
    time_spend = end_time - start_time
    print('bubble sort time used: {}'.format(time_spend) )


    