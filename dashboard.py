import streamlit as st
import matplotlib.pyplot as plt
from grpolab.storage import Storage
from grpolab.visualization import Visualizer
from grpolab.analysis import Analyzer

def format_run_option(run):
    run_id, run_name, status = run
    return f"{run_id} - {run_name} ({status})"


def display_run_information(run_details):
    st.subheader("Run Information")

    if run_details is None:
        st.warning("Run information is unavailable.")
        return

    run_id, run_name, status, start_time, end_time = run_details

    with st.container(border=True):
        first_row = st.columns(3)
        first_row[0].metric("Run ID", run_id)
        first_row[1].metric("Run Name", run_name)
        first_row[2].metric("Status", status)

        second_row = st.columns(2)
        second_row[0].metric("Start Time", start_time or "—")
        second_row[1].metric("End Time", end_time or "—")


def main():
    st.set_page_config(
        page_title="GRPO-Lab",
        page_icon="📈",
        layout="wide",
    )

    st.title("GRPO-Lab")
    st.caption("GRPO Experiment Tracking Dashboard")

    storage = Storage()
    visualizer = Visualizer(storage)
    runs = storage.get_runs()

    if not runs:
        st.warning("No experiment runs are available.")
        return

    with st.sidebar:
        st.header("Experiment Controls")
        selected_run = st.selectbox(
            "Run",
            options=runs,
            format_func=format_run_option,
        )

        run_id = selected_run[0]
        metric_names = storage.get_metric_names(run_id)

        if metric_names:
            selected_metric = st.selectbox(
                "Metric",
                options=metric_names,
            )
        else:
            selected_metric = None
            st.warning("The selected run has no metrics.")

    run_details = storage.get_run_details(run_id)
    display_run_information(run_details)

    st.subheader("Metric Visualization")
    with st.container(border=True):
        if selected_metric is None:
            st.info("Select a run with metrics to create a visualization.")
            return


        if st.button("Visualize Metric", type="primary"):
            fig = visualizer.plot_metric(run_id, selected_metric)

            if fig is None:
                st.warning("The selected metric contains no data.")
            else:
                st.pyplot(fig)
                plt.close(fig)


if __name__ == "__main__":
    main()
