import os

def base_file_name_generator():
    base_dir ="/Users/kwierman/Data/"
    for volt in os.listdir(base_dir):
        this_dir = os.path.join(base_dir, volt)
        file_name_list = [i for i in os.listdir(this_dir) if ".root" in i ]
        if len(file_name_list)>0:
            file_name = sorted(file_name_list, key=lambda x: -os.path.getctime(os.path.join(this_dir, x)))[0]
            yield {"accelerating_voltage": float(volt), "file_name": os.path.join(this_dir,file_name) }

def file_name_filter(input):
    return input["accelerating_voltage"]>-26 and input["accelerating_voltage"]<-23


class TFFilenameGenerator:
    def __init__(self):
        self.iterator = base_file_name_generator()
        self.file_name_filter = file_name_filter
    def __iter__(self):
        return self
    def __next__(self):
        return self.next()
    def next(self):
        data_pack = next(self.iterator)
        while not self.file_name_filter(data_pack):
            data_pack = next(self.iterator)
        return data_pack
