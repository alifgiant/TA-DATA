import os
import wfdb
import json
from collections import Counter
import annotations

# # all samples
# numbers = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119, 121, 122,
#            123, 124, 200, 201, 202, 203, 205, 207, 208, 209, 210, 212, 213, 214, 215, 217, 219, 220, 221, 222, 223,
#            228, 230, 231, 232, 233, 234]

# 100s
numbers = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119, 121, 122, 123, 124]

# # 200s
# numbers = [200, 201, 202, 203, 205, 207, 208, 209, 210, 212, 213, 214, 215, 217, 219, 220, 221, 222, 223, 228, 230, 231, 232, 233, 234]

# # Test samples
# numbers = [100]

if __name__ == '__main__':    
    beat_ann_all = []
    for number in (str(x) for x in numbers):
        record_name = number + '/' + number
        annotator = 'atr'
        samp_from = 0
        samp_to = None
        # record = wfdb.rdsamp(record_name, sampfrom=samp_from, sampto=samp_to)
        record = wfdb.srdsamp(record_name, sampfrom=samp_from, sampto=samp_to)
        annotation = wfdb.rdann(record_name, annotator, sampfrom=samp_from, sampto=samp_to)

        # # signal
        # print(record[0])

        # wfdb.plotrec(record, annotation=annotation, title='Record '+ number +' from MIT-BIH Arrhythmia Database',
        #              timeunits='seconds')

        beat = [(x, y) for x, y in zip(annotation.annsamp, annotation.anntype) if y in annotations.BEAT_ANNOTATION4]
        # beat = [(x, y) for x, y in zip(annotation.annsamp, annotation.anntype) if y in annotations.BEAT_ANNOTATION]
        beat_pos = [x for x, y in beat]
        beat_ann = [y for x, y in beat]

        beat_ann_all += beat_ann
        
        # # non_beat = [(x, y) for x, y in zip(annotation.annsamp, annotation.anntype) if y in annotations.NON_BEAT_ANNOTATION]
        # non_beat = [(x, y) for x, y in zip(annotation.annsamp, annotation.anntype) if y in ['[']]
        # non_beat_pos = [x for x, y in non_beat]
        # non_beat_ann = [y for x, y in non_beat]
        #
        # print('MIT_BIH/' + number, len(beat), len(non_beat))
        # print('MIT_BIH/' + number, len(beat))
        # # print('MIT_BIH/' + number, len(non_beat))

        # # count = Counter(annotation.anntype)
        count_beat_ann = Counter(beat_ann)

        categories = [['N', '/', 'L', 'R', 'Q', 'f', 'x'], ['V'], ['!']]

        count_cat = {1: 0, 2: 0, 3: 0}

        for idx, cat in enumerate(categories):
            for tipe in cat:
                if tipe in count_beat_ann:
                    count_cat[idx+1] += count_beat_ann[tipe]

        
        # # print(len(record[0]))
        # print(number, count_beat_ann)
        print(number, count_cat)
        # # print(beat_only_pos)
        # # print(beat_only_ann)
        # #
        # process beat location to peak feed
        beat_loc = [0] * len(record[0])
        for x in beat_pos:
            beat_loc[x] = 1
        
        # file_output_add = number + '/beat.json'
        file_output_add = number + '/beat2.json'
        # file_output2_add = number+'/beat_class/raw.json'
        # #
        # directory = os.path.dirname(file_output2_add)
        # if not os.path.exists(directory):
        #     print('creating', directory)
        #     os.makedirs(directory)
        # #
        json.dump(beat_loc, open(file_output_add, 'w'))
        # json.dump(beat_ann, open(file_output2_add, 'w'))

    count_beat_ann = Counter(beat_ann_all)
    print('ALL', count_beat_ann)
