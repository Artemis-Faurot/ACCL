$$
\begin{align}
    [\text{prog}] &\to [\text{stmt}]^* \\
    [\text{stmt}] &\to
    \begin{cases}
        \text{exit [expr]}; \\
        \text{let identifier: type = [expr]}; \\
        \text{def identifier([expr]*): type \{[stmt*]\}}; \\
    \end{cases} \\
    [\text{expr}] &\to
    \begin{cases}
        \text{int\_lit} \\
        \text{float\_lit} \\
        \text{str\_lit} \\
        \text{bool} \\
        \text{type} \\
        \text{identifier} \\
    \end{cases} \\
\end{align}
$$