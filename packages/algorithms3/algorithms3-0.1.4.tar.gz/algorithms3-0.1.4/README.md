Data Structures and Algorithms
==============================
 
This repository contains my implementations of data structures and algorithms using Python 3. Most of the algorithm questions are taken from LeetCode. This is a work in progress.

## Install
You can use this as an API in your code as follows:

	$ pip3 install algorithms3

An example of running an algorithm:

```python3
#Check if a string containing brackets is valid or not
#Returns bool value

from algorithms.stack import valid_paran

if __name__ == '__main__':
	isValid = valid_paran('()[]')
	print(isValid)
```

If an algorithm is listed in this repository but is not in the pip package, it means that I have not uploaded the latest version. I will be doing that once a week. 

## Uninstall
If you want to uninstall, simply run:

	$pip3 uninstall algorithms3

## Tests
I have written basic tests for most of the modules. To run all the tests at once run:
	
	$python3 -m unittest discover tests

## List of Implementations

* [Binary Search Tree](algorithms/bst)
	* [Binary Search Tree Implementation](algorithms/bst/bst.py)
	* [Recover BST swapped nodes](algorithms/bst/recover_bst.py)

* [Hash Tables](algorithms/hashtables)
	* [Two Sum](algorithms/hashtables/two_sum.py)

* [Linked List](algorithms/linkedlist)
	* [Singly Linked List implementation](algorithms/linkedlist/singly_linked_list.py)
	* [Add two numbers as Linked List](algorithms/linkedlist/add_two_numbers.py)
	* [Merge k lists](algorithms/linkedlist/merge_k_lists.py)
	* [Merge 2 lists](algorithms/linkedlist/merge_two_lists.py)
	* [Remove nth node from end](algorithms/linkedlist/remove_nth_end.py)

* [Stack](algorithms/stack)
	* [Check Valid Paranthesis](algorithms/stack/valid_paran.py)

* [Strings](algorithms/strings)
	* [Integer to Roman](algorithms/strings/int_to_roman.py)
	* [Roman to Integer](algorithms/strings/roman_to_int.py)
	* [Check integer palindrome](algorithms/strings/palindrome.py)
	* [Reverse Integer](algorithms/strings/reverse_int.py)
	* [Longest Common Prefix](algorithms/strings/longest_common_prefix.py)


