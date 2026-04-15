import pytest
import pandas as pd
from app import app, generate_figure

# ---------- UI TESTS ---------------------------#

# Test for header
def test_header_present(dash_duo):
    dash_duo.start_server(app)

    header = dash_duo.find_element("h1")
    assert header is not None
    assert "Soul Foods" in header.text

# Test for graph
def test_graph_present(dash_duo):
    dash_duo.start_server(app)

    graph = dash_duo.find_element("#line-graph")
    assert graph is not None

# Test for region picker
def test_region_picker_present(dash_duo):
    dash_duo.start_server(app)

    radio = dash_duo.find_element("#region-dropdown")
    assert radio is not None


# ---------------CALLBACK TESTS ---------------------#

# EXTRA TESTS
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Sales": [100, 200, 150, 300],
        "Date": pd.to_datetime([
            "2026-01-01",
            "2026-01-02",
            "2026-01-03",
            "2026-01-04"
        ]),
        "Region": ["north", "west", "west", "north"]
    })

# Test for all regions
def test_generate_figure_all(sample_df):
    fig = generate_figure("all", sample_df)

    assert len(fig.data) == 2
    assert "All Regions" in fig.layout.title.text

# Test for single region (north)
def test_generate_figure_single_region(sample_df):
    fig = generate_figure("north", sample_df)

    assert len(fig.data) == 1
    assert "North" in fig.layout.title.text
    assert fig.data[0].name == "north"

# Negative test: region not found
def test_generate_figure_invalid_region(sample_df):
    fig = generate_figure("invalid", sample_df)

    assert len(fig.data) == 0

def test_generate_figure_empty_df():
    empty_df = pd.DataFrame(columns=["Sales", "Date", "Region"])

    fig = app("all", empty_df)

    assert len(fig.data) == 0