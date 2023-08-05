import os
import cv2

from stagesep2.analyser.base import BaseAnalyser
from stagesep2.config import MatchTemplateConfig

# standard cross frame
standard_cross_png = os.path.join(os.path.dirname(__file__), 'cross.png')
standard_cross_frame = cv2.imread(standard_cross_png, cv2.COLOR_BGR2BGRA)


class CrossAnalyser(BaseAnalyser):
    """ (for android) if cross line existed """
    name = 'cross'

    # binary setting
    middle_value = 100
    max_value = 255
    threshold_method = cv2.THRESH_BINARY

    temp_num = 100

    @classmethod
    def _threshold_filter(cls, frame):
        binary_frame = cv2.adaptiveThreshold(frame, cls.max_value, cv2.ADAPTIVE_THRESH_MEAN_C, cls.threshold_method, 5, 5)
        binary_frame = cv2.Canny(binary_frame, 30, 150)
        cv2.imwrite('./temp/{}.png'.format(cls.temp_num), frame)
        cls.temp_num += 1
        return binary_frame

    @classmethod
    def run(cls, frame, ssv):
        binary_frame = cls._threshold_filter(frame)
        res = cv2.matchTemplate(standard_cross_frame, binary_frame, MatchTemplateConfig.cv_method)
        min_val, max_val, _, _ = cv2.minMaxLoc(res)
        return {
            'min': min_val,
            'max': max_val,
        }
