import six
from abc import ABCMeta, abstractmethod
from eyewitness.config import RAW_IMAGE_PATH, IMAGE_ID_STR_TEMPLATE


class ImageId(object):
    """
    ImageId is used to standardize the image_id format
    """

    def __init__(self, channel, timestamp, file_format='jpg'):
        """
        Parameters
        ----------
        channel: str
            channel of image comes
        timestamp: int
            timestamp of image arrive time
        format: str
            type of image
        """
        self.timestamp = timestamp
        self.channel = channel
        self.file_format = file_format

    def __hash__(self):
        return hash(self.timestamp) ^ hash(self.channel) ^ hash(self.file_format)

    def __str__(self):
        return IMAGE_ID_STR_TEMPLATE.format(
            channel=self.channel, timestamp=str(self.timestamp), file_format=self.file_format)

    def __eq__(self, other):
        if isinstance(other, ImageId):
            return str(self) == str(other)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, ImageId):
            return str(self) < str(other)
        return NotImplemented

    @classmethod
    def from_str(cls, image_id_str):
        """
        serialize image_id from string, the seperator of image is double dash --

        Parameters
        ----------
        image_id_str: str
            a string with pattern {chanel}--{timestamp}--{fileformat}

            e.g: "channel--12345567--jpg" (seperated by double dash)

        Returns
        -------
        image_id: ImageId
            a ImageId obj
        """
        # TODO make a more safer way
        if len(image_id_str.split('--')) == 3:
            channel, timestamp, file_format = image_id_str.split('--')
        else:
            channel, timestamp, file_format = (image_id_str, 0, 'jpg')
        return cls(channel=channel, timestamp=int(timestamp), file_format=file_format)


@six.add_metaclass(ABCMeta)
class ImageRegister():
    def register_image(self, image_id, meta_dict):
        """
        interface for ImageRegister to register_image
        """
        raw_image_path = meta_dict.get(RAW_IMAGE_PATH, None)
        self.insert_image_info(image_id, raw_image_path=raw_image_path)

    @abstractmethod
    def insert_image_info(image_id, raw_image_path):
        """
        abstract method which need to be implement: how to insert/record image information

        Parameters
        ----------
        image_id: ImageId
            ImageId obj
        raw_image_path: str
            the path of raw image
        """
        pass
