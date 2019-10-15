# calc
This is an interpreter for algebraic expressions. A live demonstration:

~~~
> 1
1
> (20 + 1) * 2
42
> foo
unknown variable at :0
> foo = 1
1
> foo + 2
3
~~~

The help page lists all features:

~~~
> help()
OPERATIONS
  a     variable lookup
a = b   variable assignment
a + b   add
a - b   subtract
a * b   multiply
a / b   divide
bar()   function call
 (a)    group

FUNCTIONS
help()  print help
exit()  terminate
~~~
