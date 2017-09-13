head -n 7987 cleaned_dataset.csv > malicious.csv
split -l 7987 cleaned_dataset.csv
rm xaa
cat x* > genuine_whole.csv
gshuf genuine_whole.csv > genuine_shuffled.csv
head -n 47000 genuine_shuffled.csv > genuine.csv
cat malicious.csv genuine.csv > whole_dataset.csv
# edit columns in excel as outlined in report
split -l 64549 whole_dataset.csv
mv xaa training.csv
mv xab testing.csv