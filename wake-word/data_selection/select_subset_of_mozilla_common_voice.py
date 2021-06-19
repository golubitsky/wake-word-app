import csv
import os
import re

# Developed with the following:
#  pip3 install boto3==1.17.84
import boto3


# To use this file:
# 0. Download and unzip the Mozilla Voice Dataset; set paths in the constants below.
# 1. Follow instructions in `s3_bucket` below to authenticate w/S3.
# 2. Review constants below, particularly note TARGET_WORD, which will determine which data are uploaded.
# 3. Execute:
# python3 data_selection/select_subset_of_mozilla_common_voice.py

# Load the TSV file
# Filter rows whose 'sentence' value matches a regular expression
#   Downcase strings before searching.
#   2 Regexes for three data subsets:
#   1. Regex to find instances of the word, e.g. "down" (positive)
#   2. Regex to find instances of the word within other words, e.g. "downstairs" (confusing negative)
#   3. At random select other ones that don't match either — v.1 strategy: enough to balance the dataset. (negative)
# Load the MP3 file at the 'path' value for each row
# Upload each MP3 file to S3 bucket.
# Upload an index of all uploaded files, same TSV format as Mozilla, except add column 'subset', as explained above.


MOZILLA_COMMON_VOICE_CLIPS_DIR = '/Users/mikegolubitsky/Documents/capstone_data/cv-corpus-6.1-2020-12-11/en/clips'
MOZILLA_TSV_FILES_DIR = '/Users/mikegolubitsky/Documents/capstone_data'

# test.tsv is a small file that is useful for development
SOURCE_TSV_FILENAME = 'validated.tsv'

TARGET_WORD = 'down'

S3_BUCKET_NAME = 'hey-spotify'
DESTINATION_DIR = f'input_audio/mozilla/{TARGET_WORD}'

SUBSETS = ['positive', 'confusing_negative', 'negative']


def s3_bucket(bucket_name):
    # First, setup per https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html
    s3 = boto3.resource('s3')

    matched = [bucket for bucket in s3.buckets.all() if bucket.name == bucket_name]

    if len(matched) == 1:
        return matched[0]
    else:
        raise RuntimeError('Found either 0 or more than 1 matching buckets')


def read_tsv(path_to_tsv_file):
    with open(path_to_tsv_file) as file:
        return list(csv.reader(file, delimiter="\t", quotechar='"'))


def write_tsv(filename, labels, rows):
    with open(filename, 'wt') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(labels)
        for row in rows:
            tsv_writer.writerow(row)


def regex_by_name(name):
    return {
        'positive': rf'[^a-z]{TARGET_WORD}[^a-z]|[^a-z]{TARGET_WORD}$|^{TARGET_WORD}[^a-z]|^{TARGET_WORD}$',
        # Ignore the possibility of punctuation around the target word.
        'confusing_negative': rf'[a-z]{TARGET_WORD}|{TARGET_WORD}[a-z]'
    }[name]


def matched_rows(tsv_rows, regex):
    matched_rows = []

    # first row is labels, so ignore it
    for row in tsv_rows[1:]:
        sentence = row[2].lower()  # to use case-insensitive regexes

        if re.search(regex, sentence) is not None:
            matched_rows.append(row)

    return matched_rows


def negative_examples(tsv_contents, all_matched_examples):
    # Return same number of examples as in positive examples
    count_positive_examples = len(all_matched_examples['positive'])

    # Exclude both positive and confusing_negative examples.
    positive_filenames = [row[1] for row in all_matched_examples['positive']]
    confusing_negative_filenames = [row[1] for row in all_matched_examples['confusing_negative']]
    filenames_to_exclude = set(positive_filenames + confusing_negative_filenames)

    # Otherwise, return examples at random.
    matched_rows = []

    # first row is labels, so ignore it
    for row in tsv_contents[1:]:
        if row[1] in filenames_to_exclude:
            continue
        matched_rows.append(row)

        if len(matched_rows) == count_positive_examples:
            return matched_rows


def upload_mp3_files_to_s3(all_rows, bucket):
    count_rows = len(all_rows)
    print(f"Uploading {count_rows} examples of target word '{TARGET_WORD}'")

    for index, row in enumerate(all_rows):
        mp3_filename = row[1]
        sentence = row[2].lower()
        subset = row[10]

        # Sanity checks.
        assert(subset in SUBSETS)
        if subset == 'negative':
            assert(TARGET_WORD not in sentence)
        else:
            assert(TARGET_WORD in sentence)

        print(f"Uploading {index+1} of {count_rows} ({mp3_filename}): ({subset}) {sentence}")
        source_path = os.path.join(MOZILLA_COMMON_VOICE_CLIPS_DIR, mp3_filename)
        destination_path = os.path.join(DESTINATION_DIR, subset, mp3_filename)
        bucket.upload_file(source_path, destination_path)


def main():
    # Store the positive and confusing_negative results, to exclude them from negative results
    all_matched_examples = {}

    # Determine matched examples belonging to each of the three subsets.
    # Each example will be uploaded.
    # Subsets: positive, confusing_negative, negative are described above
    tsv_filepath = os.path.join(MOZILLA_TSV_FILES_DIR, SOURCE_TSV_FILENAME)
    for subset_name in ['positive', 'confusing_negative']:
        print(f"Finding matches for '{subset_name}' subset for target word '{TARGET_WORD}'")

        # Open tsv file provided by Mozilla
        tsv_contents = read_tsv(tsv_filepath)

        # Filter Mozilla file for only sentences containing target word, according to subsets (defined above).
        regex = regex_by_name(subset_name)
        matched_examples_rows = matched_rows(tsv_contents, regex)
        all_matched_examples[subset_name] = matched_examples_rows

    print(f"Finding matches for '{subset_name}' subset for target word '{TARGET_WORD}'")
    all_matched_examples['negative'] = negative_examples(tsv_contents, all_matched_examples)

    # Prepare CSV file containing index of all examples
    index_tsv_filename = f'{TARGET_WORD}.tsv'
    print(f"Uploading metadata {index_tsv_filename}")

    # Append subset column.
    labels = tsv_contents[0] + ['subset']

    # Compile rows for all subsets; also add the subset name to the last column.
    all_rows = []
    for subset_name in SUBSETS:
        rows_for_subset = all_matched_examples[subset_name]
        for row in rows_for_subset:
            all_rows.append(row + [subset_name])

    # Upload index and mp3 files.
    bucket = s3_bucket(S3_BUCKET_NAME)

    write_tsv(index_tsv_filename, labels, all_rows)
    destination_path = os.path.join(DESTINATION_DIR, index_tsv_filename)
    bucket.upload_file(index_tsv_filename, destination_path)

    upload_mp3_files_to_s3(all_rows, bucket)


if __name__ == "__main__":
    main()
