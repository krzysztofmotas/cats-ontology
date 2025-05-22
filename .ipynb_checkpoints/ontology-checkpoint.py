from cognipy.ontology import Ontology, encode_string_for_graph_label
import textwrap

def graph_attribute_formatter(val):
    if isinstance(val, list) or isinstance(val, set):
        return " | ".join(list(map(lambda i: encode_string_for_graph_label(graph_attribute_formatter(i)), val)))
    elif isinstance(val, dict):
        return " | ".join(list(map(lambda i: i[0] + " : " + encode_string_for_graph_label(graph_attribute_formatter(i[1])), val.items())))
    else:
        return encode_string_for_graph_label(textwrap.fill(str(val), 40))

onto = Ontology("cnl/file", "cats.encnl",
                evaluator=lambda e: eval(e, globals(), locals()),
                graph_attribute_formatter=graph_attribute_formatter)

onto.draw_graph(layout="hierarchical")

