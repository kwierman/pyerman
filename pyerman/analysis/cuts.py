class PenningTrapDataSet(object):
    def __init__(self, x_up, y_up, x_down, y_down, x_up_err, y_up_err, x_down_err, y_down_err):
        self.xup = x_up
        self.yup = y_up
        self.xdown = x_down
        self.ydown = y_down
        self.xuperr = x_up_err
        self.yuperr = y_up_err
        self.xdownerr = x_down_err
        self.ydownerr = y_down_err

    def reverse_data_set(self, down=True):
        """Usually  you want to do this to the 'down' data set as the baseline fits the skewed gaussian better
        """
        if down:
            self.ydown = [ i for i in reversed(self.ydown)]
            self.ydownerr =[i for i in reversed(self.ydownerr) ]
        else:
            self.yup = [ i for i in reversed(self.yup)]
            self.yuperr =[i for i in reversed(self.yuperr) ]

    def subruncut_simple(self, down=True,threshold=100):
        """
        defines a simple cut to look for the threshold at the beginning of each subrun and cut out the point
        """
        if down:
            length = len(self.xdown)
            removal_indices=[]
            for i in range(1,length):
                if self.ydown[i]-self.ydown[i-1]>threshold:
                    removal_indices.append(i)
            for i in reversed(removal_indices):
                self.xdown.pop(i)
                self.ydown.pop(i)
                self.xdownerr.pop(i)
                self.ydownerr.pop(i)
        else:
            length = len(self.xup)
            removal_indices=[]
            for i in range(1,length):
                if self.yup[i]-self.yup[i-1]>threshold:
                    removal_indices.append(i)
            for i in reversed(removal_indices):
                self.xup.pop(i)
                self.yup.pop(i)
                self.xuperr.pop(i)
                self.yuperr.pop(i)

    def threshold_matching(self, threshold=100):
        """looks for the threshold at the beginning of each data set and slices each data set to match the threshold
        """
        first_index=0
        second_index =0

        for i in range(1,len(self.yup)):
            if self.yup[i]-self.yup[i-1]>threshold:
                first_index=i
                break
        for i in range(1,len(self.ydown)):
            if self.ydown[i]-self.ydown[i-1]>threshold:
                second_index=i
                break
        diff = abs(first_index-second_index)
        if(second_index<first_index):
            self.xdown = [i+diff for i in self.xdown ]
            self.xdownerr = [ i for i in self.xdownerr ]
        else:
            self.xup    = [i+diff for i in self.xup ]
            self.xuperr = [i for i in self.xuperr ]
        return first_index, second_index
