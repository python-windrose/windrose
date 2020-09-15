import matplotlib
import numpy as np
import pandas as pd
from numpy.testing import assert_allclose
from pandas.testing import assert_frame_equal

from windrose import clean, clean_df, plot_windrose
from windrose import DEFAULT_THETA_LABELS

matplotlib.use("Agg")  # noqa
# Create wind speed and direction variables
N = 500
ws = np.random.random(N) * 6
wd = np.random.random(N) * 360

df = pd.DataFrame({"speed": ws, "direction": wd})


def test_windrose_pd_not_default_names():
    kind = "scatter"
    df_not_default_names = pd.DataFrame({"wind_speed": ws, "wind_direction": wd})
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
        }
    )
    actual_df = clean_df(df)
    expected_df = pd.DataFrame(
        {
            "direction": [1.0],
            "speed": [2.0],
        }
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