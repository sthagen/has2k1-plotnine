import numpy as np
import pandas as pd

from plotnine import (
    aes,
    annotate,
    facet_grid,
    facet_wrap,
    geom_abline,
    geom_path,
    geom_point,
    ggplot,
)
from plotnine.data import mpg, mtcars

n = 10
df = pd.DataFrame(
    {
        "x": range(n),
        "y": range(n),
        "var1": np.repeat(range(n // 2), 2),
        "var2": np.tile(["a", "b"], n // 2),
    }
)
df["class"] = df["var1"]  # python keyword as column
df["g"] = df["var1"]  # variable as a column

g = ggplot(df, aes("x", "y")) + geom_point(
    aes(color="factor(var1)"), size=5, show_legend=False
)


# facet_wrap


def test_facet_wrap_one_var():
    p = g + facet_wrap("~var1")
    p2 = g + facet_wrap("~class")  # python keyword in formula
    p3 = g + facet_wrap("~g")  # variable in formula
    assert p == "facet_wrap_one_var"
    assert p2 == "facet_wrap_one_var"
    assert p3 == "facet_wrap_one_var"


def test_facet_wrap_expression():
    p = g + facet_wrap("pd.cut(var1, (0, 2, 4), include_lowest=True)")
    assert p == "facet_wrap_expression"


def test_facet_wrap_two_vars():
    p = g + facet_wrap("~var1+var2")
    p2 = g + facet_wrap("~class+var2")  # python keyword in formula
    assert p == "facet_wrap_two_vars"
    assert p2 == "facet_wrap_two_vars"


def test_facet_wrap_label_both():
    p = g + facet_wrap("~var1+var2", labeller="label_both")
    assert p == "facet_wrap_label_both"


def test_facet_wrap_not_as_table():
    p = g + facet_wrap("~var1", as_table=False)
    assert p == "facet_wrap_not_as_table"


def test_facet_wrap_direction_v():
    p = g + facet_wrap("~var1", dir="v")
    assert p == "facet_wrap_direction_v"


def test_facet_wrap_not_as_table_direction_v():
    p = g + facet_wrap("~var1", as_table=False, dir="v")
    assert p == "facet_wrap_not_as_table_direction_v"


# facet_grid


def test_facet_grid_one_by_one_var():
    p = g + facet_grid("var1~var2")
    p2 = g + facet_grid("class~var2")  # python keyword in formula
    assert p == "facet_grid_one_by_one_var"
    assert p2 == "facet_grid_one_by_one_var"


def test_facet_grid_expression():
    p = g + facet_grid(
        ["var2", "pd.cut(var1, (0, 2, 4), include_lowest=True)"]
    )
    assert p == "facet_grid_expression"


def test_facet_grid_margins():
    p = g + facet_grid("var1~var2", margins=True)
    assert p == "facet_grid_margins"


def test_facet_grid_scales_free_y():
    p = g + facet_grid("var1>2 ~ x%2", scales="free_y")
    assert p == "facet_grid_scales_free_y"


def test_facet_grid_formula_with_dot():
    p = g + facet_grid(". ~ var1>2")
    assert p == "facet_grid_formula_with_dot"


def test_facet_grid_formula_without_dot():
    p = g + facet_grid("~var1>2")
    assert p == "facet_grid_formula_with_dot"


def test_facet_grid_scales_free_x():
    p = g + facet_grid("var1>2 ~ x%2", scales="free_x")
    assert p == "facet_grid_scales_free_x"


def test_facet_grid_drop_false():
    df = mpg.copy()
    df["drv"] = pd.Categorical(df["drv"], ["4", "f", "r", "Q"])

    p = (
        ggplot(df, aes(x="displ", y="hwy"))
        + geom_point()
        + facet_grid("drv ~ .", drop=False)
    )
    assert p == "facet_grid_drop_false"


def test_facet_grid_space_ratios():
    p = (
        ggplot(mtcars, aes("wt", "mpg"))
        + geom_point()
        + facet_grid("am ~ vs", space={"y": [1, 2], "x": [1, 2]})
    )
    assert p == "facet_grid_space_ratios"


# Edge cases


def test_non_mapped_facetting():
    p = g + geom_abline(intercept=0, slope=1, size=1) + facet_wrap("var1")
    assert p == "non_mapped_facetting"


def test_dir_v_ncol():
    p = (
        ggplot(mpg)
        + aes(x="displ", y="hwy")
        + facet_wrap("class", dir="v", ncol=4, as_table=False)
        + geom_point()
    )
    assert p == "dir_v_ncol"


def test_variable_and_annotate():
    p = (
        g
        + annotate("point", x=4.5, y=5.5, color="cyan", size=10)
        + facet_wrap("~g")
    )
    assert p == "variable_and_annotate"


def test_manual_mapping_with_lists():
    p = (
        g
        + annotate(
            "abline", intercept=[4, 10], slope=[-1, -1], color=["red", "blue"]
        )
        + facet_wrap("var1")
    )
    assert p == "manual_mapping_with_lists"


def test_array_mapping_and_evaluation():
    # GH548
    # When we map to array/series of values, the aes evaluation
    # should not mix up the values.
    df = pd.DataFrame({"x": range(12), "y": range(12), "g": list("abcd") * 3})

    # should be the same as if color='g'
    p = (
        ggplot(df, aes("x", "y", color=df["g"]))
        + geom_point(size=4)
        + geom_path()
        + facet_wrap("~g")
    )
    assert p == "array_mapping_and_evaluation"
