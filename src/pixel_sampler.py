import numpy as np
from args_parser import ArgsParser
from image_generator import ImageGenerator

class PixelSampler:

    def __init__(self, args=None):
        self.args = ArgsParser(args)
        self.image_generator = ImageGenerator(self.get_ascii_image())

    def get_ascii_image(self):
        self.args.check_for_invalid_args()
        
        img_arr = self.args.get_resized_bw_img()
        charset = self.args.get_charset()

        ptgs = self.get_ptgs(len(charset))
        ascii_arr = [[" " for _ in range(img_arr.shape[1])] for _ in range(img_arr.shape[0])]

        for i, ptg in enumerate(ptgs):
            last_ptg = ptgs[i-1] if i > 0 else 0

            lt_idxs = self.tuple_set(np.argwhere(img_arr < ptg * 255).tolist())
            gt_idxs = self.tuple_set(np.argwhere(img_arr >= last_ptg * 255).tolist())

            idxs = list(set(lt_idxs).intersection(gt_idxs))
            for idx in idxs:
                ascii_arr[idx[0]][idx[1]] = charset[i]*2
        
        return self.flatten_2d_str_array(ascii_arr)

    def get_ptgs(self, n):
        sampler = self.args.get_sampler()
        lower_ptg = self.args.get_lower_ptg()
        upper_ptg = self.args.get_upper_ptg()

        if sampler == "linear":
            return [0] + np.linspace(lower_ptg, upper_ptg, n-2).tolist() + [1]
        elif sampler == "log":
            return np.logspace(lower_ptg, upper_ptg, n-1).tolist() + [1]
        elif sampler == "exp":
            return np.exp(np.linspace(lower_ptg, upper_ptg, n-1)).tolist() + [1]
        else:
            raise ValueError("Invalid sampler.")

    def tuple_set(self, seq):
        return {tuple(item) for item in seq}

    def flatten_2d_str_array(self, arr):
        return ["".join(row) for row in arr]