import streamlit as st
import pandas as pd


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv("titanic_train.csv")


def compute_missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    total_rows = len(df)
    summary = df.isna().sum().rename("Количество пропусков").to_frame()
    summary["Процент пропусков (%)"] = (
        summary["Количество пропусков"] / total_rows * 100
    ).round(2)
    summary["Всего записей"] = total_rows
    return summary.reset_index().rename(columns={"index": "Столбец"})


def filter_summary(summary: pd.DataFrame, only_missing: bool) -> pd.DataFrame:
    if not only_missing:
        return summary
    return summary[summary["Количество пропусков"] > 0]


def sort_summary(summary: pd.DataFrame, option: str) -> pd.DataFrame:
    if option == "По убыванию доли пропусков":
        return summary.sort_values(
            by=["Процент пропусков (%)", "Столбец"], ascending=[False, True]
        )
    return summary.sort_values(by="Столбец")


def main() -> None:
    st.set_page_config(
        page_title="Пропуски в данных Титаника",
        page_icon="🚢",
        layout="centered",
    )

    df = load_data()

    st.title("Пропуски в данных Титаника")
    st.write(
        "Просмотрите таблицу по всем столбцам и "
        "при необходимости выберите конкретный столбец для подробностей."
    )

    summary = compute_missing_summary(df)
    only_missing = st.checkbox(
        "Показывать только столбцы с пропусками", value=True)
    summary = filter_summary(summary, only_missing)

    sort_option = st.selectbox(
        "Сортировка:",
        (
            "По убыванию доли пропусков",
            "По возрастанию названия столбца",
        ),
    )
    summary = sort_summary(summary, sort_option)

    st.dataframe(summary, use_container_width=True)


if __name__ == "__main__":
    main()
