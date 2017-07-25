from collections import Counter
import wfdb
import json
import sample
import MIT_BIH.annotations


def view_waveform(address, samp_from, samp_to, annotation):
    wfdb_record = wfdb.rdsamp(address, sampfrom=samp_from, sampto=samp_to)  # native, not support indexing
    wfdb.plotrec(wfdb_record, annotation=annotation, title='Record ' + address + ' from MIT-BIH Arrhythmia Database',
                 timeunits='seconds')


def extract_beat(annotation, beat_annotation):
    beats = [(x, y) for x, y in zip(annotation.annsamp, annotation.anntype) if y in beat_annotation]
    beat_pos = [x for x, y in beats]
    beat_type = [y for x, y in beats]
    return beat_pos, beat_type


def show_current_beat_types(name, beat_type):
    count_beat_type = Counter(beat_type)
    print(name, count_beat_type)


def tsipouras_beat_class(name, beat_type):
    # tsipouras class
    categories = [['.', 'N', '/', 'L', 'R', 'Q', 'f'], ['V', 'A', 'a', 'J', 'S', 'F', 'x'], ['!']]

    count_beat_type = Counter(beat_type)
    count_cat = {1: 0, 2: 0, 3: 0}
    for idx, cat in enumerate(categories):
        for clazz in cat:
            if clazz in count_beat_type:
                count_cat[idx + 1] += count_beat_type[clazz]

    print(name, count_cat)


def output_beat_location(address, samp_from, samp_to, beat_pos, output_address):
    wfdb_record = wfdb.srdsamp(address, sampfrom=samp_from, sampto=samp_to)  # support indexing

    beat_loc = [0] * len(wfdb_record[0])

    for x in beat_pos:
        beat_loc[x] = 1

    beat_loc_add = address[:-3] + output_address
    json.dump(beat_loc, open(beat_loc_add, 'w'))
    print('created', beat_loc_add)


def purge(dir, pattern):
    import os, re
    for f in os.listdir(dir):
        if re.search(pattern, f):
            os.remove(os.path.join(dir, f))

    print('deleted', dir + '/' + pattern)


if __name__ == '__main__':
    source = sample.MitBih
    base = sample.MitBih.base
    output_loc_address = 'beat_loc.json'

    '''..........................Select Source.................................'''
    records = source.get_all_record()             # all records
    # records = source.get_record_series_100()      # 100s records
    # records = source.get_record_series_200()      # 200s records
    # records = source.get_one_record(num=100)      # record number 100
    '''........................................................................'''

    '''..........................Select Annotator.................................'''
    # beat_annotation = MIT_BIH.annotations.BEAT_ANNOTATION4    # Same annotation as paper of M.G Tsipouras
    # beat_annotation = MIT_BIH.annotations.BEAT_ANNOTATION3    # Same annotation as physionet
    # beat_annotation = MIT_BIH.annotations.BEAT_ANNOTATION2    # Same annotation as MIT BIH Arrhythmia Dataset
    beat_annotation = MIT_BIH.annotations.BEAT_ANNOTATION     # Same beat count as MIT BIH Arrhythmia Dataset
    '''...........................................................................'''

    all_beat_type = []

    for record in records:
        str_record = str(record)
        print(str_record)

        record_address = base + '/' + str_record + '/' + str_record
        annotator = 'atr'
        samp_from = 0
        samp_to = None

        annotation = wfdb.rdann(record_address, annotator, sampfrom=samp_from, sampto=samp_to)
        # view_waveform(record_name, samp_from, samp_to, annotation)  # view wave plot

        beat_pos, beat_type = extract_beat(annotation, beat_annotation)
        all_beat_type += beat_type  # hold all beat

        # show_current_beat_types(str_record, beat_type)  # show beat type
        # tsipouras_beat_class(str_record, beat_type)  # show tsipouras beat class

        output_beat_location(record_address, samp_from, samp_to, beat_pos, output_loc_address)  # output beat loc
        # purge(base+'/'+str_record, output_loc_address)  # delete output beat loc
        # purge(base+'/'+str_record, 'samples.csv')  # delete other thing

    count_all_beat_type = Counter(all_beat_type)
    print('ALL', count_all_beat_type)

