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


def format_percent(value):
    if value is None:
        return "N/A"
    return f"{value}%"


def display_response_snapshot(title, snapshot):
    st.markdown(f"#### {title}")

    with st.container(border=True):
        metric_columns = st.columns(2)
        metric_columns[0].metric("Step", snapshot["step"])
        metric_columns[1].metric("Reward", snapshot["reward"])

        st.markdown("Response")
        st.info(snapshot["response"])


def display_behavioral_evolution_result(result):
    if result["status"] != "success":
        st.warning(result.get("message", "No behavioral evolution data found."))
        return

    earliest_column, latest_column = st.columns(2)
    with earliest_column:
        display_response_snapshot("Earliest Response", result["earliest"])

    with latest_column:
        display_response_snapshot("Latest Response", result["latest"])

    summary = result["learning_summary"]

    st.markdown("#### Learning Summary")
    summary_columns = st.columns(3)
    reward_change = summary["reward_change"]
    reward_pct = summary["reward_change_percent"]

    reward_change_display = f"+{reward_change}" if reward_change > 0 else str(reward_change)
    reward_pct_display = f"+{reward_pct}%" if reward_pct and reward_pct > 0 else f"{reward_pct}%"

    summary_columns[0].metric("Reward Change", reward_change_display)
    summary_columns[1].metric("Reward Improvement %", reward_pct_display)
    summary_columns[2].metric(
        "Training Steps Observed",
        summary["steps_observed"],
    )

    if summary["improved"]:
        st.success("The response improved over the observed training window.")
    else:
        st.warning("No reward improvement was observed over the training window.")


def display_metric_viewer(run_id, selected_metric, visualizer):
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


def display_behavioral_evolution(run_id, storage, analyzer):
    st.subheader("Behavioral Evolution")

    prompts = storage.get_unique_prompts(run_id)
    if not prompts:
        st.info("No behavioral rollout data has been logged for this run.")
        st.stop()
    selected_prompt = st.selectbox(
        "Training Prompt",
        options=prompts,
    )

    with st.container(border=True):
        result = analyzer.analyze_behavioral_evolution(
            run_id,
            selected_prompt,
        )
        display_behavioral_evolution_result(result)


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
    analyzer = Analyzer(storage)
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

    metric_viewer_tab, behavioral_evolution_tab = st.tabs(
        ["📈 Metric Viewer", "🧠 Behavioral Evolution"]
    )

    with metric_viewer_tab:
        display_metric_viewer(run_id, selected_metric, visualizer)

    with behavioral_evolution_tab:
        display_behavioral_evolution(run_id, storage, analyzer)


if __name__ == "__main__":
    main()
