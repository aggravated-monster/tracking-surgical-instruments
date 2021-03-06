import tsi.tsi_sys as tsic
import phase8_lstm_common as p8
import pandas as pd


def get_input_base():
    return 'c:/ou/output/phase7/7_sweeps_corrected/'

def get_output_base():
    return 'c:/ou/output/phase8/lstm/large/2-classes-instrument-x/'

def get_output_figures_base():
    return get_output_base() + "figures/"

def get_output_figure_name(prefix, suffix):
    return get_output_figures_base() + prefix + '_' + suffix + '.png'

def get_output_file_name(suffix):
    return get_output_base() + suffix + '_large_labeled_lstm_dataset.csv'

def get_labels_exp1():
    return 'c:/ou/input/phase7/rings.csv'

def get_labels_exp2():
    return 'c:/ou/input/phase7/rings_experiment2.csv'

def get_predictions_file_name(suffix):
    return get_output_base() + suffix + '_predictions.csv'

def get_aggregates_file_name(suffix):
    return get_output_base() + suffix + '_aggregates.csv'

  
def pre_process(input_file_path, df_labels, prefix, sweep):

    pos_dict = { 'B': 0.01,
                 'E': 0.02,
                 'A': 0.03
    }

    # load the dataframe
    df_in = pd.read_csv(input_file_path)

    # take oonly the position columns
    #df_pos = df_in[['position_tool' ,'position_eye', 'subject', 'name']]
    df_pos = df_in[['eye_x' ,'tooltip_x', 'subject', 'name']]

    # drop the rows without name
    df_pos = df_pos[df_pos['name'].notna()]

    # drop the unknowns
    #df_pos = df_pos[df_pos['position_tool'] != 'U']
    #df_pos = df_pos[df_pos['position_eye'] != 'U']
    #df_pos = df_pos[df_pos['eye_x'].notna()]
    df_pos = df_pos[df_pos['tooltip_x'].notna()]
    #df_pos = df_pos[df_pos['tooltip_x'].notna()]

    if df_pos.empty:
        return None

    # merge in the labels
    df_pos = pd.merge(df_pos, df_labels, on=['subject'], how='left')

    # encode positions
    #df_pos["encoded tool position"] = df_pos.apply(lambda x : (pos_dict[x['position_tool']]), axis = 1)
    #df_pos["encoded eye position"] = df_pos.apply(lambda x : (pos_dict[x['position_eye']]), axis = 1)
    #df_pos["normalised eye_x"] = df_pos.apply(lambda x : x['eye_x']/1280, axis = 1)


    # now pivot the encoded position column into an array
    #position_arr = df_pos[['encoded tool position', 'encoded eye position']].to_numpy()
    #position_arr = df_pos[['encoded tool position']].to_numpy()
    #position_arr = df_pos[['encoded eye position']].to_numpy()
    #position_arr = df_pos[['normalised eye_x']].to_numpy()
    #position_arr = df_pos[['eye_x']].to_numpy()
    position_arr = df_pos[['tooltip_x']].to_numpy()
    #super lazy
    label_arr = df_pos['label'].to_numpy()

    # return
    return (prefix, sweep, label_arr[0], position_arr)



def do_experiment(df_in, learning_rate, seed):

    repetitions = 10

    X, y, label_mapping = p8.prep_x_y_lstm(df_in, ['padded sequence', 'label'])

    result_dict = {
        'model': 'lstm',
        'classes': 2,
        #'features':'encoded [tool_position]',
        #'features':'encoded [eye_position]',
        #'features':'raw [eye_x]',
        'features':'raw [tooltip_x]',
        'learning_rate': learning_rate,
        'label mapping': label_mapping
    }

    predictions = p8.run_predictions(X, y, seed, repetitions, learning_rate, get_output_figure_name, 1)

    aggregates = p8.calculate_aggregates(predictions)
    result_dict['aggregates'] = aggregates
    result_dict['predictions'] = predictions

    return result_dict


if __name__ == "__main__":

    result = []
    experiment_results = []

    input_folders = tsic.list_folders(get_input_base())

    tsic.make_dir(get_output_base())
    tsic.make_dir(get_output_figures_base())

    for input_folder in input_folders:

        # strip inner folder and prepare output folder
        suffix = tsic.get_basename(input_folder)
        # get labels
        if suffix == "experiment1":
            df_labels = pd.read_csv(get_labels_exp1())
            df_labels = df_labels[["Su", "groups"]]
            # rename Su
            df_labels.rename(columns={'Su': 'subject'}, inplace=True)
            df_labels.rename(columns={'groups': 'label'}, inplace=True)
        else:
            df_labels = pd.read_csv(get_labels_exp2(), delimiter=";")
            df_labels = df_labels[["subject", "label"]]

        # collect the sweep folders
        sweep_folders = tsic.list_folders(input_folder)
        for sweep_folder in sweep_folders:
            prefix = tsic.get_basename(sweep_folder)
            if prefix != 'p3-1a': #p3-!a has no gaze positions and has been excluded from the comparative experiment
                # collect the sweeps
                input_files = tsic.list_files(sweep_folder)
                for input_file in input_files:
                    sweep = tsic.drop_path_and_extension(input_file)
                    print("Sequencing: " + sweep)
                    res = pre_process(input_file, df_labels, prefix, sweep)
                    if res != None:
                        result.append(res)
        
        df = pd.DataFrame(result, columns=['subject', 'sweep', 'label', 'sequence'])

        # drop the mediums
        df = df[df['label'] != "Medium"]

        df = p8.apply_padding(df)
        df.to_csv(get_output_file_name(suffix), index=False)

        #learning_rates = [0.00001]
        learning_rates = [0.0001]

        for learning_rate in learning_rates:
            # placeholder for summary0.01
            res = do_experiment(df, learning_rate, 7)
            experiment_results.append(res)
            # write intermediate because of terribly long runtime
            df_result = pd.DataFrame(experiment_results)

            df_predictions = df_result[['model','classes','features','label mapping','learning_rate', 'predictions']]
            df_aggregates = df_result[['model','classes','features','label mapping','learning_rate','aggregates']]

            df_predictions.to_csv(get_predictions_file_name(suffix), index=False)
            df_aggregates.to_csv(get_aggregates_file_name(suffix), index=False)


    print('*** LSTM modeling and evaluation completed ***')
