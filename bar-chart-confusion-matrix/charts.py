import altair as alt

from utils import compute_confusion_categories


def confusion_matrix(data, score_var, target_var, threshold):
    data = compute_confusion_categories(data, score_var, target_var, threshold)
    return data
