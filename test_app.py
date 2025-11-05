import pandas as pd
from app import compute_missing_summary, filter_summary, sort_summary


def make_df():
    return pd.DataFrame(
        {
            "A": [1, None, 3],
            "B": [None, None, 2],
            "C": [1, 2, 3],
        }
    )


# Проверяет, что сводка корректно считает пропуски, проценты и общее число строк
def test_compute_missing_summary_counts_and_percentages():
    df = make_df()
    summary = compute_missing_summary(df)

    assert summary.loc[summary["Столбец"] ==
                       "A", "Количество пропусков"].item() == 1
    assert summary.loc[summary["Столбец"] ==
                       "B", "Количество пропусков"].item() == 2
    assert summary.loc[summary["Столбец"] ==
                       "C", "Количество пропусков"].item() == 0
    assert summary["Всего записей"].unique().tolist() == [len(df)]
    assert summary.loc[summary["Столбец"] == "B",
                       "Процент пропусков (%)"].item() == 66.67


# Проверяет, что фильтрация корректно работает (выбор столбцов только с пропусками)
def test_filter_summary_only_missing_removes_full_columns():
    df = make_df()
    summary = compute_missing_summary(df)
    filtered = filter_summary(summary, only_missing=True)

    assert set(filtered["Столбец"]) == {"A", "B"}
    assert "C" not in filtered["Столбец"].values


# Проверяет, что без фильтрации возвращаются все столбцы, включая полные
def test_filter_summary_all_columns_when_disabled():
    df = make_df()
    summary = compute_missing_summary(df)
    filtered = filter_summary(summary, only_missing=False)

    assert set(filtered["Столбец"]) == {"A", "B", "C"}


# Проверяет, что сортировка зависит от выбранной пользователем опции
def test_sort_summary_respects_selected_option():
    df = make_df()
    summary = compute_missing_summary(df)

    by_missing = sort_summary(summary, "По убыванию доли пропусков")
    assert by_missing["Столбец"].tolist()[:2] == ["B", "A"]

    alphabetical = sort_summary(summary, "По возрастанию названия столбца")
    assert alphabetical["Столбец"].tolist() == ["A", "B", "C"]
