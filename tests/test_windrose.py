import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
from numpy.testing import assert_allclose
from pandas.testing import assert_frame_equal

from windrose import (
    DEFAULT_THETA_LABELS,
    WindroseAxes,
    clean,
    clean_df,
    plot_windrose,
)

matplotlib.use("Agg")  # noqa
# Create wind speed and direction variables
N = 500
ws = np.random.random(N) * 6
wd = np.random.random(N) * 360

df = pd.DataFrame({"speed": ws, "direction": wd})


def test_windrose_pd_not_default_names():
    kind = "scatter"
    df_not_default_names = pd.DataFrame(
        {"wind_speed": ws, "wind_direction": wd},
    )
    plot_windrose(
        df_not_default_names,
        kind=kind,
        alpha=0.2,
        var_name="wind_speed",
        direction_name="wind_direction",
    )


def test_windrose_clean():
    direction = np.array([1.0, 1.0, 1.0, np.nan, np.nan, np.nan])
    var = np.array([2.0, 0.0, np.nan, 2.0, 0.0, np.nan])
    actual_direction, actual_var = clean(direction, var)
    expected_direction = np.array([1.0])
    expected_var = np.array([2.0])
    assert_allclose(actual_direction, expected_direction)
    assert_allclose(actual_var, expected_var)


def test_windrose_clean_df():
    df = pd.DataFrame(
        {
            "direction": [1.0, 1.0, 1.0, np.nan, np.nan, np.nan],
            "speed": [2.0, 0.0, np.nan, 2.0, 0.0, np.nan],
        },
    )
    actual_df = clean_df(df)
    expected_df = pd.DataFrame(
        {
            "direction": [1.0],
            "speed": [2.0],
        },
    )
    assert_frame_equal(actual_df, expected_df)


def test_theta_labels():
    # Ensure default theta_labels are correct
    ax = WindroseAxes.from_ax()
    theta_labels = [t.get_text() for t in ax.get_xticklabels()]
    assert theta_labels == DEFAULT_THETA_LABELS
    plt.close()

    # Ensure theta_labels are changed when specified
    ax = WindroseAxes.from_ax(theta_labels=list("abcdefgh"))
    theta_labels = [t.get_text() for t in ax.get_xticklabels()]
    assert theta_labels == ["a", "b", "c", "d", "e", "f", "g", "h"]
    plt.close()


@pytest.mark.parametrize("kind", ["bar", "box", "contour", "contourf"])
@pytest.mark.parametrize("normed, suffix", [(False, ""), (True, "%")])
def test_radial_label_units(kind, normed, suffix):
    data = pd.DataFrame({"direction": [0, 90], "speed": [1, 2]})
    ax = plot_windrose(data, kind=kind, normed=normed)
    try:
        expected = (
            ["10%", "20%", "30%", "40%", "50%"]
            if normed
            else [
                "0.2",
                "0.4",
                "0.6",
                "0.8",
                "1.0",
            ]
        )
        assert [tick.get_text() for tick in ax.get_yticklabels()] == expected

        ax.set_rmax(12.5)
        ax.set_radii_angle(angle=90)
        expected = [f"{r:.1f}{suffix}" for r in (2.5, 5, 7.5, 10, 12.5)]
        assert [tick.get_text() for tick in ax.get_yticklabels()] == expected

        ax.clear()
        ax.set_rmax(10)
        ax.set_radii_angle()
        assert [tick.get_text() for tick in ax.get_yticklabels()] == [
            "2",
            "4",
            "6",
            "8",
            "10",
        ]
    finally:
        plt.close(ax.figure)


def test_tex_radial_labels_escape_percent_sign():
    ax = WindroseAxes.from_ax()
    try:
        ax.bar(np.array([0, 90]), np.array([1, 2]), normed=True)
        ax.set_radii_angle(usetex=True)
        assert ax.get_yticklabels()[-1].get_text() == r"50\%"
    finally:
        plt.close(ax.figure)


def test_windrose_incorrect_bins_specified():
    ax = WindroseAxes.from_ax()
    with pytest.raises(ValueError) as exc_info:
        ax.bar(direction=wd, var=ws, bins=[1, 2, 3])

    (msg,) = exc_info.value.args
    assert msg == (
        "the first value provided in bins must be less than or equal to the minimum "
        "value of the wind speed data. Did you mean: bins=(0, 1, 2, 3) ? "
        "If you want to exclude values below a certain threshold, "
        "try setting calm_limit=1."
    )


def test_windrose_incorrect_bins_in_combination_with_calm_limit():
    ax = WindroseAxes.from_ax()
    with pytest.raises(ValueError) as exc_info:
        ax.bar(direction=wd, var=ws, bins=[1, 2, 3], calm_limit=2)

    (msg,) = exc_info.value.args
    assert msg == "the lowest value in bins must be >= 2 (=calm_limits)"
