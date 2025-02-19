
import subprocess

import numpy as np
from sklearn.model_selection import KFold
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


#gor1, gor3, gor4
#gor_method = "gor1"

# paths to JAR files
validate_jar_path = "C:/Users/test/PycharmProjects/propra24/crossVal/validate.jar"

#parameters:
#no parameters:
train_jar_path = "C:/Users/test/PycharmProjects/propra24/crossVal/train.jar"
#predict_jar_path = "C:/Users/test/PycharmProjects/propra24/crossVal/predict.jar"

#pseudocounts:
#train_jar_path = "C:/Users/test/IdeaProjects/propra24/out/artifacts/ParameterTuning/pseudoCounts/1/train.jar"
#predict_jar_path = "C:/Users/test/IdeaProjects/propra24/out/artifacts/ParameterTuning/pseudoCounts/1/predict.jar"

#windowsize C:\Users\test\IdeaProjects\propra24\out\artifacts\ParameterTuning\windowSize\11
#train_jar_path = "C:/Users/test/IdeaProjects/propra24/out/artifacts/ParameterTuning/windowSize/11/train.jar"
#predict_jar_path = "C:/Users/test/IdeaProjects/propra24/out/artifacts/ParameterTuning/windowSize/11/predict.jar"

#postprocessing
predict_jar_path = "C:/Users/test/IdeaProjects/propra24/out/artifacts/ParameterTuning/Postprocessing/triple/predict.jar"

# paths to data files
validation_data_path = "C:/Users/test/PycharmProjects/propra24/crossVal/cb513.db"
#valSummary_file = "C:/Users/test/PycharmProjects/propra24/crossVal/valSummary.txt" #currently not sved as file
#valDetailed_file = "C:/Users/test/PycharmProjects/propra24/crossVal/valDetailed.txt"

# run train.jar
def train_model(input_path, output_path, method):
    subprocess.run(["java", "-jar", train_jar_path, "--db", input_path, "--model", output_path, "--method", method])

# run predict.jar
def predict(input_model_path, txt_html, input_seq_path):
    subprocess.run(["java", "-jar", predict_jar_path, "--model", input_model_path, "--seq", input_seq_path, "--format", txt_html])

#  run validate.jar and get mean Q3 and Sov values
def validate(prediction_file, sec_structure_file, summary_file, detailed_file): #save mean q3 and mean sov +(H E C)
    subprocess.run(["java", "-jar", validate_jar_path, "--p", prediction_file, "--r", sec_structure_file, "--f", "txt", "--s", summary_file, "--d", detailed_file])
    validation_results = {}
    with open(summary_file, 'r') as summary:
        for line in summary:
            if line.startswith("q3 :"):
                parts = line.strip().split(':')
                meanQ3 = float(parts[2].split()[0].strip())
                validation_results['q3'] = meanQ3
            elif line.startswith("SOV"):
                parts = line.strip().split(':')
                sov_name = parts[0].strip()
                mean_value = float(parts[2].split()[0].strip())
                validation_results[sov_name] = mean_value
    return validation_results



#  load data from the data file
def load_data(data_path):
    with open(data_path, 'r') as file:
        lines = file.readlines()
    data = []
    i = 0
    while i < len(lines):
        # Skip empty lines
        if lines[i].strip() == '':
            i += 1
            continue
        # Extract ID, AS, and SS
        id = lines[i].strip()[1:]
        AS = lines[i+1].strip()[3:]
        SS = lines[i+2].strip()[3:]
        data.append((id, AS, SS))
        i += 3
    return data


gor_methods = ["gor1", "gor3", "gor4"]
#gor_methods = ["gor1"]
# Initialize fold_results with keys for each GOR method and empty lists for the performance metrics
fold_results = {gor_method: {key: [] for key in ["q3", "SOV", "SOV_H", "SOV_E", "SOV_C"]} for gor_method in gor_methods}
 #nested dict to store each folds result for each gorX

for gor_method in gor_methods:  # loop all gors

    kf = KFold(n_splits=5, random_state=42, shuffle=True)  # 5-fold cross-val
    fold_performance = []

    # Load data cb513.db
    data = load_data(validation_data_path)


    for fold, (train_index, test_index) in enumerate(kf.split(data), 0):  # kf.split returns (train, test) tupels (indexing start at 0)
        train_data = [data[i] for i in train_index]
        test_data = [data[i] for i in test_index]

        #train_split_path = "C:/Users/test/PycharmProjects/propra24/crossVal/train_split.txt"
        # Write train and test data to temporary files
        with open('train_split.txt', 'w') as train_file:
            for id, seq, ss in train_data:
                train_file.write(f">{id}\nAS {seq}\nSS {ss}\n\n")

        with open('test_split.txt', 'w') as test_file:
            for id, seq, ss in test_data:
                test_file.write(f">{id}\nAS {seq}\nSS {ss}\n\n") #format: AS; PS for validate jar


        trained_model_path = "C:/Users/test/PycharmProjects/propra24/crossVal/model.txt"  # gets created by train.jar for every gor1,3,4
        # Train the model
        train_model('train_split.txt', trained_model_path, gor_method)  # (input_path, output_path, method)

        #convert seclib to fasta for predict.jar
        def seclib_to_fasta(data):
            adjusted_data = []
            for entry in data:  # only get id and AS
                id = entry[0]
                AS = entry[1]
                adjusted_data.append((id, AS))
            return adjusted_data

        testData = load_data('test_split.txt')  # load test seclib data
        testDataFasta = seclib_to_fasta(testData)  # turn into fasta format

        with open('test_split_fasta.txt', 'w') as file:  # save fasta data to a file
            for id, sequence in testDataFasta:
                file.write(f">{id}\n{sequence}\n")


        # run predict.jar and capture output to a file
        def run_predict_and_save_output(input_model_path, txt_html, input_seq_path, output_file):
            java_command = ['java', '-jar', predict_jar_path, '--model', input_model_path, '--seq', input_seq_path,
                            '--format', txt_html]
            java_output = subprocess.check_output(java_command).decode('utf-8', 'ignore')

            with open(output_file, 'w') as predictFile:
                predictFile.write(java_output)

        prediction_file = 'C:/Users/test/PycharmProjects/propra24/crossVal/prediction.txt' #save prediction of each fold in prediction.txt
        run_predict_and_save_output(trained_model_path,   "txt", 'test_split_fasta.txt', prediction_file)

        summary_file = 'summary.txt'
        detailed_file = 'detailed.txt'
        # validateGOR.jar: CAREFUL: (predictionFile: AS, PS & secStrucFile: AS, SS)
        validation_results = validate(prediction_file, 'test_split.txt', summary_file, detailed_file)
        # Store individual results for each fold with the gor version
        for key, value in validation_results.items():
            fold_results[gor_method][key].append(value)

        # Append SOV means to fold_performance
        for sov_name, sov_mean in validation_results.items():
            if sov_name.startswith("SOV"):
                fold_performance.append(sov_mean)


print(fold_results)
#print("Postprocessing singular and double and triple:")
print("Postprocessing singular and double and triple:")
for gor_method, metrics in fold_results.items():
    print(f"Mean results for {gor_method}:")
    for metric, values in metrics.items():
        mean_value = np.mean(values)
        print(f"{metric}: {mean_value:.2f}")
    print()  # Add a blank line for readability between GOR methods



# Convert the nested dictionary to a DataFrame
data_list = []
for gor_method, metrics in fold_results.items():
    for fold_number, values in enumerate(metrics['SOV']):  # Assuming SOV is the key for fold performance
        data_list.append({
            'GOR Method': gor_method,
            'Fold Number': fold_number + 1,  # Assuming fold number starts at 1
            'SOV Score': values  # Replace this with the actual key if different
        })

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(data_list)

# Create the Seaborn plot
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
# Create a barplot with GOR Method on the x-axis, the SOV Score on the y-axis,
# and each bar grouped by Fold Number
plot = sns.barplot(x='GOR Method', y='SOV Score', hue='Fold Number', data=df, palette='viridis')

#plt.title('Mean SOV evaluated with 5-fold Cross Validation with Pseudocount = 1')
#plt.title('Mean SOV with Postprocessing to remove singular and double occurences of H and E + triple occurences of H')
plt.title('Mean SOV with Postprocessing to remove singular  occurences of H and E')
plt.xlabel('GOR Version')
plt.ylabel('SOV')

# Save the plot
plt.savefig('C:/Users/test/PycharmProjects/propra24/crossVal/Postprocessing_triple.png')
#plt.savefig('C:/Users/test/PycharmProjects/propra24/crossVal/mean_SOV_scores_plot_triplePostprocess.png')


"""

#Q3:

# Convert nested dictionary to DataFrame
q3_data_list = []
for gor_method, metrics in fold_results.items():
    for fold_number, value in enumerate(metrics['q3']):  # Assuming 'q3' is the key for Q3 performance
        q3_data_list.append({
            'GOR Method': gor_method,
            'Fold Number': fold_number + 1,  # Assuming fold number starts at 1
            'Q3 Score': value
        })

# Create a DataFrame
q3_df = pd.DataFrame(q3_data_list)

sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
q3_plot = sns.barplot(x='GOR Method', y='Q3 Score', hue='Fold Number', data=q3_df, palette='viridis')

plt.title('Mean Q3 of GOR Versions evaluated with 5-fold Cross Validation')
plt.title('Mean Q3 ')
plt.xlabel('GOR Version')
plt.ylabel('Q3 Score')

#plt.savefig('C:/Users/test/PycharmProjects/propra24/crossVal/q3_mean_folds_plot_pseudocount1.png')
plt.savefig('C:/Users/test/PycharmProjects/propra24/crossVal/Q3_CrossVal_new title.png')
#plt.show()

"""