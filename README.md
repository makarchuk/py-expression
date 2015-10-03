Parse math expression into a tree.

```
$ python expression.py
(x^3 - x)^2*(x+168)*(123x-27+18*(24x^2-6)^4) + 1+x
+       operation
        *       operation
                ^       operation
                        -       operation
                                ^       operation
                                        x       variable
                                        3.0     number
                                x       variable
                        2.0     number
                *       operation
                        +       operation
                                x       variable
                                168.0   number
                        +       operation
                                -       operation
                                        *       operation
                                                123.0   number
                                                x       variable
                                        27.0    number
                                *       operation
                                        18.0    number
                                        ^       operation
                                                -       operation
                                                        *       operation
                                                                24.0    number
                                                                ^       operation
                                                                        x       variable
                                                                        2.0     number
                                                        6.0     number
                                                4.0     number
        +       operation
                1.0     number
                x       variable
```