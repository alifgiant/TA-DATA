class MitBih(object):
    base = 'MIT_BIH'
    records = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119, 121, 122,
               123, 124, 200, 201, 202, 203, 205, 207, 208, 209, 210, 212, 213, 214, 215, 217, 219, 220, 221, 222, 223,
               228, 230, 231, 232, 233, 234]

    @staticmethod
    def get_one_record(num=100):
        # all record
        if num not in MitBih.records:
            raise Exception('Record not exist')

        records = [num]
        return records

    @staticmethod
    def get_all_record():
        # all record
        for record in MitBih.records:
            yield record

    @staticmethod
    def get_record_series_100():
        # series 100 records
        for record in MitBih.records:
            if record < 200:
                yield record

    @staticmethod
    def get_record_series_200():
        # series 200 records
        for record in MitBih.records:
            if record >= 200:
                yield record

if __name__ == '__main__':
    pass
