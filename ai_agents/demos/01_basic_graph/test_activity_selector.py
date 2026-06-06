from unittest.mock import patch

from activity_selector import create_activity_graph, decide_mood_node


def test_decide_mood_node_returns_node_2_when_choice_is_surfing():
    with patch("activity_selector.random.choice", return_value="node_2"):
        assert decide_mood_node({"graph_state": "Vikkas will"}) == "node_2"


def test_decide_mood_node_returns_node_3_when_choice_is_climbing():
    with patch("activity_selector.random.choice", return_value="node_3"):
        assert decide_mood_node({"graph_state": "Vikkas will"}) == "node_3"


def test_decide_mood_node_picks_from_valid_nodes():
    with patch("activity_selector.random.choice", return_value="node_2") as mock_choice:
        decide_mood_node({"graph_state": "x"})
        mock_choice.assert_called_once_with(["node_2", "node_3"])


def test_graph_invoke_routes_to_rock_climbing():
    graph = create_activity_graph()
    with patch("activity_selector.random.choice", return_value="node_3"):
        result = graph.invoke({"graph_state": "Vikkas"})
    assert result["graph_state"] == "Vikkas will go rock climbing"
