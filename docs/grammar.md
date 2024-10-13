$$
\begin{align}
    [\text{prog}] &\to \text{[stmt]*} \\
    [\text{stmt}] &\to
    \begin{cases}
        \text{exit [expr];} \\
        \text{let identifier: type = [expr];} \\
    \end{cases} \\
    [\text{expr}] &\to
    \begin{cases}
        \text{int\_lit} \\
        \text{identifier} \\
        \text{[binary\_expr]} \\
    \end{cases} \\
    [\text{binary\_expr}] &\to
    \begin{cases}
        \text{[expr] * or / [expr] prec = 1} \\
        \text{[expr] + or - [expr] prec = 0} \\
    \end{cases} \\
\end{align}
$$