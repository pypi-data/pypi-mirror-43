# pytest

## EXPERIMENTAL

The code defines cell magic %%pytest evaluates
the current cell as a test case

~~~
def foo():
    return True

def bar():
    return False

~~~
%%pytest
assert foo()
~~~
~~~
.
[100%]
1 passed in 0.02 seconds
~~~

~~~
%%pytest
assert bar()
~~~
~~~
F
[100%]
================================================================================ FAILURES =================================================================================
________________________________________________________________________________ test_In_8 ________________________________________________________________________________

    def test_In_8():
>       assert bar()
E       assert False
E        +  where False = bar()

/tmp/test_j0xocmx9.py:10: AssertionError
1 failed in 0.12 seconds

~~~

