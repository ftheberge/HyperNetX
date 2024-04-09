import pandas as pd

from hypernetx.classes.hyp_view import HypergraphView
from hypernetx.classes.incidence_store import IncidenceStore
from hypernetx.classes.property_store import PropertyStore


def test_to_dataframe_with_no_user_defined_properties():
    # Create a HypergraphView with no user-defined properties
    incidence_df = pd.DataFrame(incidences(), columns=["edges", "nodes"])
    hyp_view = HypergraphView(
        IncidenceStore(incidence_df), level=2, property_store=PropertyStore()
    )

    # Create the expected dataframe
    expected_dfp = pd.DataFrame(
        index=incidences(), data={"weight": 1, "misc_properties": [{}]}
    )
    expected_dfp.sort_index(inplace=True)

    actual_dfp = hyp_view.to_dataframe
    actual_dfp.sort_index(inplace=True)

    # compare the actual and expected dataframes
    # there should be no differences and thus the resulting dataframe is empty
    assert actual_dfp.compare(expected_dfp).empty

    # The total number of items in the properties dataframe should be equal to the total number of incidences
    assert len(actual_dfp) == len(incidence_df)

    # On the other hand, the hypergraph_view properties should be empty since the user did not define any properties for any items
    assert len(hyp_view.properties) == 0


def test_to_dataframe_with_user_defined_properties():
    # Create a HypergraphView with user-defined properties
    incidence_df = pd.DataFrame(incidences(), columns=["edges", "nodes"])
    ps_df = pd.DataFrame(index=[(0, "A")], data={"weight": 42, "misc_properties": [{}]})
    hyp_view = HypergraphView(
        IncidenceStore(incidence_df), level=2, property_store=PropertyStore(ps_df)
    )

    # create the expected dataframe
    expected_dfp = pd.DataFrame(
        index=incidences(), data={"weight": 1, "misc_properties": [{}]}
    )
    expected_dfp.at[(0, "A"), "weight"] = 42
    expected_dfp.sort_index(inplace=True)

    actual_dfp = hyp_view.to_dataframe
    actual_dfp.sort_index(inplace=True)

    # compare the actual and expected dataframes
    # there should be no differences and thus the resulting dataframe is empty
    df_diffs = actual_dfp.compare(expected_dfp)
    assert df_diffs.empty

    # The total number of items in the properties dataframe should be equal to the total items in the incidence store
    assert len(actual_dfp) == len(incidence_df)

    # On the other hand, the user defined properties for one item, (0,'A')
    assert len(hyp_view.properties) == 1


def incidences():
    node_groups = [
        {"A", "B"},
        {"A", "C"},
        {"A", "B", "C"},
        {"A", "D", "E", "F"},
        {"D", "F"},
        {"E", "F"},
        {"B"},
        {"G", "B"},
    ]
    # creates a dictionary of edges to list of nodes
    edges_to_nodes = dict(enumerate(node_groups))

    # create a list of all edge to node pairs (i.e. incidences)
    # The total number of incidences will be 18
    incidences_ = []
    for edge, nodes in edges_to_nodes.items():
        for node in nodes:
            incidences_.append((edge, node))

    return incidences_
