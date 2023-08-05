from loguru import logger
from skimage.measure import compare_ssim
import cv2
import numpy as np

import os


class IPDPicture(object):
    def __init__(self, pic_path):
        self.path = os.path.abspath(pic_path)
        self.data = None
        self.width = None
        self.height = None

        self._load_from_path()

    def _load_from_path(self):
        assert os.path.isfile(self.path), 'file {} not found'.format(self.path)
        self.data = cv2.imread(self.path, flags=cv2.IMREAD_GRAYSCALE)
        self.width, self.height, *_ = self.data.shape
        logger.debug('{} loaded'.format(str(self)))

    def __str__(self):
        return '<IPDPicture {}x{} from {}>'.format(self.width, self.height, self.path)

    def cal(self, color_num: int = None) -> float:
        return compare_ssim(_build_pure_pic(self.width, self.height, color_num), self.data)


def _build_pure_pic(width: int, height: int, color: int) -> np.ndarray:
    raw = np.zeros((width, height), np.uint8)
    raw.fill(color)
    return raw


def detect(pic_path, color_num):
    logger.debug('analysing picture: [{}]'.format(pic_path))
    ipd_pic = IPDPicture(pic_path)
    return ipd_pic.cal(color_num)
