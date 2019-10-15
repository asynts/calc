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
> -(1 + 2)
-3
~~~

The help page lists all features:

~~~
> help()
OPERATIONS
name
name = expr
name()

-expr
(expr)

expr + expr
expr - expr
expr * expr
expr / expr

FUNCTIONS
help()
exit()
~~~
