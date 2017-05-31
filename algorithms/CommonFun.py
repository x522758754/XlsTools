#!user/bin/env python
# coding:utf-8

import sys
import random

reload(sys)
sys.setdefaultencoding('utf-8')

def QuickSort(left, right, array):
	l = left
	r = right
	while l < r:
		base = array[r]
		while (array[l] <= base and l < r):
			l = l + 1
		if(l < r):
			array[r] = array[l]

		while (array[l] <= array[r] and l < r):
			r = r - 1
		if(l < r):
			array[l] = array[r]
		
		array[r] = base
		QuickSort(left, r - 1, array)
		QuickSort(r + 1, right, array)

#array 为有序数组
def BinarySearch(left, right, array, target):
	if(left < right):
		mid = (left + right)/2
		if(array[mid] > target):
			return BinarySearch(left, mid-1, array, target)
		elif(array[mid] < target):
			return BinarySearch(mid+1, right, array, target)
		else:
			return mid
	else:
		return -1

if __name__ == '__main__':
	array = []
	for i in range(10):
		it = random.randint(1, 100)
		array.append(it)

	QuickSort(0, len(array)-1, array)

	print BinarySearch(0, len(array)-1, array, 15)