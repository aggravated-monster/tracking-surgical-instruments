import pandas as pd
import tsi.tsi_sys as tsis
import phase8_svm_common as p8

CLASSES = 3

def get_output_base():
    return 'd:/ou/output/phase8/svm/experiment/large/' + str(CLASSES) + '-classes/'

def get_output_figures_base():
    return get_output_base() + "figures/"

def get_output_figure_name(prefix, suffix):
    return get_output_figures_base() + prefix + '_' + suffix + '.png'

def get_input_file():
    # the large dataset
    return 'd:/ou/output/phase7/9_large_labeled_dataset/large_labeled_dataset.csv'

def get_predictions_file_name():
    return get_output_base() + 'predictions.csv'

def get_aggregates_file_name():
    return get_output_base() + 'aggregates.csv'


def evaluate_highest_singles(classes, df):

    result = []

    # highest single from research features
    features = ['count_fixation_duration']
    res, df_acc = p8.evaluate_group(10, "rbf", df, features, "single", "research", classes, 7)
    result.append(res)

    # highest single from gaze features
    features = ['sum_abs_delta_eye_x']
    res, df_acc = p8.evaluate_group(10, "rbf", df, features, "single", "gaze", classes, 7, df_acc)
    result.append(res)

    # highest single from instrument features
    features = ['sum_abs_delta_tooltip_x']
    res, df_acc = p8.evaluate_group(10, "rbf", df, features, "single", "instrument", classes, 7, df_acc)
    result.append(res)

    # highest single from spatial features
    features = ['sum_abs_x_distance']
    res, df_acc = p8.evaluate_group(100, "rbf", df, features, "single", "spatial", classes, 7, df_acc)
    result.append(res)

    # highest single from temporal features
    features = ['fixation_streak']
    res, df_acc = p8.evaluate_group(10, "rbf", df, features, "single", "temporal", classes, 7, df_acc)
    result.append(res)

    p8.plot_boxplot("highest-single", df_acc, get_output_figure_name)

    return result

def evaluate_highest_pairs(classes, df):

    # highest pair from research features
    features = ['count_fixation_duration', 'sum_fixation_duration']
    res, df_acc = p8.evaluate_group(1, "rbf", df, features, "pair", "research", classes, 167)
    result.append(res)

    p8.plot_scatterplot("highest-pair", df[features], features, 'research', get_output_figure_name)

    # highest pair from gaze features
    features = ['sum_abs_delta_eye_x', 'sum_abs_delta_eye_y']
    res, df_acc = p8.evaluate_group(10, "rbf", df, features, "pair", "gaze", classes, 167, df_acc)
    result.append(res)

    p8.plot_scatterplot("highest-pair", df[features], features, 'gaze', get_output_figure_name)

    # highest pair from instrument features
    features = ['sum_abs_delta_tooltip_x', 'sum_abs_delta_tooltip_y']
    res, df_acc = p8.evaluate_group(0.1, "rbf", df, features, "pair", "instrument", classes, 167, df_acc)
    result.append(res)

    p8.plot_scatterplot("highest-pair", df[features], features, 'instrument', get_output_figure_name)

    # highest pair from spatial features
    features = ['sum_abs_x_distance', 'sum_abs_y_distance']
    res, df_acc = p8.evaluate_group(100, "rbf", df, features, "pair", "spatial", classes, 167, df_acc)
    result.append(res)

    p8.plot_scatterplot("highest-pair", df[features], features, 'spatial', get_output_figure_name)

    # highest pair from temporal features
    features = ['fixation_streak', 'departure_offset']
    res, df_acc = p8.evaluate_group(10, "rbf", df, features, "pair", "temporal", classes, 167, df_acc)
    result.append(res)

    p8.plot_scatterplot("highest-pair", df[features], features, 'temporal', get_output_figure_name)

    p8.plot_boxplot("highest-pair", df_acc, get_output_figure_name)

    return result

def evaluate_highest_triplet(classes, df):

    # highest triplet from research features
    features = ['mean_fixation_duration', 'min_fixation_duration', 'sum_fixation_duration']
    res, df_acc = p8.evaluate_group(100, "rbf", df, features, "triplet", "research", classes, 273)
    result.append(res)

    # highest triplet from gaze features
    features = ['sum_abs_delta_eye_x', 'sum_abs_delta_eye_y', 'sum_delta_eye_euclid']
    res, df_acc = p8.evaluate_group(100, "rbf", df, features, "triplet", "gaze", classes, 273, df_acc)
    result.append(res)

    # highest triplet from instrument features
    features = ['sum_abs_delta_tooltip_x', 'sum_abs_delta_tooltip_y', 'sum_delta_tooltip_euclid']
    res, df_acc = p8.evaluate_group(1, "rbf", df, features, "triplet", "instrument", classes, 273, df_acc)
    result.append(res)

    # highest triplet from spatial features
    features = ['sum_abs_x_distance', 'sum_abs_y_distance', 'sum_euclid_distance']
    res, df_acc = p8.evaluate_group(10, "rbf", df, features, "triplet", "spatial", classes, 273, df_acc)
    result.append(res)

    # highest triplet from temporal features
    features = ['fixation_streak', 'departure_offset', 'arrival_offset']
    res, df_acc = p8.evaluate_group(0.1, "rbf", df, features, "triplet", "temporal", classes, 273, df_acc)
    result.append(res)

    p8.plot_boxplot("highest-triplet", df_acc, get_output_figure_name)

    return result


def evaluate_highest_overall(classes, df):

    # highest overall from research features
    features = ['mean_fixation_duration', 'min_fixation_duration', 'sum_fixation_duration']
    res, df_acc = p8.evaluate_group(100, "rbf", df, features, "overall", "research", classes, 387)
    result.append(res)

    # highest overall from gaze features
    features = ['sum_abs_delta_eye_x', 'sum_abs_delta_eye_y', 'sum_delta_eye_euclid']
    res, df_acc = p8.evaluate_group(100, "rbf", df, features, "overall", "gaze", classes, 387, df_acc)
    result.append(res)

    # highest overall from instrument features
    features = ['sum_abs_delta_tooltip_x', 'sum_abs_delta_tooltip_y', 'sum_delta_tooltip_euclid']
    res, df_acc = p8.evaluate_group(1, "rbf", df, features, "overall", "instrument", classes, 387, df_acc)
    result.append(res)

    # highest overall from spatial features
    features = ['sum_abs_x_distance', 'sum_abs_y_distance']
    res, df_acc = p8.evaluate_group(100, "rbf", df, features, "overall", "spatial", classes, 387, df_acc)
    result.append(res)

    # highest overall from temporal features
    features = ['fixation_streak', 'departure_offset']
    res, df_acc = p8.evaluate_group(10, "rbf", df, features, "overall", "temporal", classes, 387, df_acc)
    result.append(res)

    p8.plot_boxplot("highest-overall", df_acc, get_output_figure_name)

    return result


if __name__ == "__main__":

    result = []
    aggregates = []

    tsis.make_dir(get_output_base())
    tsis.make_dir(get_output_figures_base())

    # load the dataframe
    df_in = pd.read_csv(get_input_file())

    # drop the mediums (for 2 classes)
    if CLASSES == 2:
        df = df_in[df_in['label'] != "Medium"]
    else:
        df = df_in

    scores = evaluate_highest_singles(CLASSES, df)
    result = result + scores

    scores = evaluate_highest_pairs(CLASSES, df)
    result = result + scores

    scores = evaluate_highest_triplet(CLASSES, df)
    result = result + scores

    scores = evaluate_highest_overall(CLASSES, df)
    result = result + scores

    df_result = pd.DataFrame(result)


    df_predictions = df_result[['model','group','feature set','classes','features','label mapping','predictions']]
    df_aggregates = df_result[['model','group','feature set','classes','features','label mapping','aggregates']]

    df_predictions.to_csv(get_predictions_file_name(), index=False)
    df_aggregates.to_csv(get_aggregates_file_name(), index=False)

   
    print('*** SVM evaluation and plotting completed ***')


