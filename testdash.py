from app import app

def test_header_is_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#app-header", timeout=10)

    header = dash_duo.find_element("#app-header")
    assert header.text == "Soul Foods Pink Morsel Sales"


def test_visualisation_is_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-chart", timeout=10)

    chart = dash_duo.find_element("#sales-chart")
    assert chart is not None


def test_region_picker_is_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#region-picker", timeout=10)

    region_picker = dash_duo.find_element("#region-picker")
    assert region_picker is not None