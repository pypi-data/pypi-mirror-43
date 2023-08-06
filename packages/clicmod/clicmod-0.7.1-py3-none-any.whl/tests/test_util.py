from util.util import preorder_traversal_dir, find_automaton_parent, find_category_parent


def sanity(x):
    return x + 1


def test_sanity():
    assert sanity(1) == 2


def test_preorder_traversal(generate_node_list):
    test_input = generate_node_list[0]
    expected_output = generate_node_list[1]
    assert preorder_traversal_dir(test_input)[0] == expected_output[0]
