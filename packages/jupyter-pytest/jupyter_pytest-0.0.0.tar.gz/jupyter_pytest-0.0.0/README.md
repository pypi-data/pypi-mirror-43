# pytest

The code defines cell magic %%pytest evaluates
the current cell as a test case

~~~
def foo():
    return True

def bar():
    return False

~~~
%%pytest -v
def test_foo()
    assert foo()
~~~

~~~
%%pytest -v
def test_bar()
    assert bar()
~~

