'''This is the "BeautifulNester.py" module and it provides one function called print_lol()
    which prints lists that may or may not include nested lists.'''
import sys
def print_lol(the_list,indent=False,level=0,fh=sys.stdout):
    '''This function takes four positional arguments, "the_list", "indent","level","fh".
       "the_list" is any Python list (of - possibly - nested lists). Each data item in the provided 
        list is (recurisively) printed to the screen on it's own line. 
        "indent" is indentation, default is False
        "level" is tab_stop, default is none
        "fh" is Standard output
    '''
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item,indent,level+1,fh)
        else:
            if indent:
                # for tabstop in range(level):
                    print("\t*level",end='',file=fh)
            print(each_item,file=fh)