$$
\begin{align}
    [\text{prog}] &\to [\text{stmt}]^* \\
    [\text{stmt}] &\to
    \begin{cases}
        \text{exit [expr]};\\
        \text{let identifier: type = [expr]};\\
    \end{cases} \\
    [\text{expr}] &\to
    \begin{cases}
        \text{int\_lit} \\
        \text{str\_lit} \\
        \text{type} \\
        \text{identifier} \\
    \end{cases} \\
\end{align}
$$