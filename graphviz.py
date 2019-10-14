import lang

class Graph:
    def __init__(self):
        self._counter = 0
        self._output = 'digraph {\n'

    def create_node(self, label) -> int:
        id_ = self._counter
        self._counter += 1

        self._output += f'\t{id_} [label="{label}"];\n'
        return id_

    def create_edge(self, from_, to):
        self._output += f'\t{from_} -> {to};\n'

    def display(self, node: lang.parser.Expr) -> int:
        if isinstance(node, lang.parser.ExprInteger):
            id0 = self.create_node(node.value)
            id1 = self.create_node('ExprInteger')
            self.create_edge(id1, id0)
            return id1
        
        if isinstance(node, lang.parser.ExprBinding):
            id0 = self.create_node('ExprBinding')

            id1 = self.create_node(node.name)
            self.create_edge(id0, id1)

            return id0
        
        if isinstance(node, lang.parser.ExprInvoke):
            id0 = self.create_node('ExprInvoke')

            id1 = self.create_node(node.name)
            self.create_edge(id0, id1)

            for argument in node.arguments:
                self.create_edge(id0, self.display(argument))
            
            return id0

        if isinstance(node, lang.parser.ExprBinary):
            id0 = self.create_node('ExprBinary')

            self.create_edge(id0, self.display(node.lhs))

            id1 = self.create_node(node.operator)
            self.create_edge(id0, id1)

            self.create_edge(id0, self.display(node.rhs))

            return id0

        raise NotImplementedError

    def finalize(self) -> str:
        return self._output + '}\n'

def create_graph(ast: lang.parser.Expr):
    graph = Graph()
    graph.display(ast)
    return graph.finalize()
