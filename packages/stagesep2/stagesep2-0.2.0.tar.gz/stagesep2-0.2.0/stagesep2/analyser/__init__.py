"""
analyser

opencv frame -> result
"""
from stagesep2.analyser.ocr import OCRAnalyser
from stagesep2.analyser.match_template import MatchTemplateAnalyser
from stagesep2.analyser.trend import TrendAnalyser
from stagesep2.analyser.cross import CrossAnalyser


ANALYSER_DICT = {
    'ocr': OCRAnalyser,
    'match_template': MatchTemplateAnalyser,
    'trend': TrendAnalyser,
    'cross': CrossAnalyser,
}
