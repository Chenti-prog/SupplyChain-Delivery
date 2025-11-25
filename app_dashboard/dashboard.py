import pandas as pd
import requests
import streamlit as st
from datetime import date
from typing import Optional


# Hard-code API URL so we don't fight env vars
API_BASE_URL = "http://localhost:8000"


def fetch_json(path: str, params: Optional[dict] = None):
    url = f"{API_BASE_URL}{path}"
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        st.error(f"Error calling API {url}: {e}")
        return None


def page_overview():
    st.header("Delivery Performance Overview")

    summary = fetch_json("/metrics/summary")
    if not summary:
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Shipments", f"{summary['total_shipments']}")
    col2.metric("On-Time Rate (%)", f"{summary['on_time_rate_pct']:.2f}")
    col3.metric("Avg Transit Hours", f"{summary['avg_transit_hours']:.2f}")

    st.subheader("On-Time Rate By Day")

    with st.expander("Filter by date range"):
        start = st.date_input("Start date", value=None)
        end = st.date_input("End date", value=None)

    params = {}
    if isinstance(start, date):
        params["start"] = start.isoformat()
    if isinstance(end, date):
        params["end"] = end.isoformat()

    daily = fetch_json("/metrics/on_time_by_day", params=params)
    if not daily:
        st.info("No daily data returned.")
        return

    df = pd.DataFrame(daily)
    df["ship_date"] = pd.to_datetime(df["ship_date"])
    df = df.sort_values("ship_date")

    st.line_chart(df.set_index("ship_date")["on_time_rate_pct"])
    st.dataframe(df, use_container_width=True)


def page_routes():
    st.header("Route Performance (Worst Destination States)")

    min_ship = st.slider("Minimum shipments required", 1, 50, 10)
    limit = st.slider("How many worst routes to show?", 5, 50, 10)

    routes = fetch_json(
        "/metrics/routes_worst",
        params={"min_shipments": min_ship, "limit": limit},
    )
    if not routes:
        st.info("No route data.")
        return

    df = pd.DataFrame(routes)

    st.subheader("Average Transit Hours by State")
    st.bar_chart(df.set_index("dest_state")["avg_transit_hours"], height=300)

    st.subheader("Detailed Table")
    st.dataframe(df, use_container_width=True)


def page_drivers():
    st.header("Driver Leaderboard")

    limit = st.slider("Top N drivers", 5, 50, 10)

    drivers = fetch_json("/drivers/leaderboard", params={"limit": limit})
    if not drivers:
        st.info("No driver data.")
        return

    df = pd.DataFrame(drivers)

    st.subheader("🏆 On-Time Rate (%) by Driver")
    st.bar_chart(df.set_index("driver_id")["on_time_rate_pct"], height=300)

    st.subheader("Driver Details")
    st.dataframe(df, use_container_width=True)


def main():
    st.set_page_config(
        page_title="Supply Chain Dashboard",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.sidebar.title("Navigation")
    st.sidebar.write("API Source:", API_BASE_URL)

    page = st.sidebar.radio(
        "Go to page",
        ("Overview", "Routes", "Drivers")
    )

    if page == "Overview":
        page_overview()
    elif page == "Routes":
        page_routes()
    elif page == "Drivers":
        page_drivers()


if __name__ == "__main__":
    main()
