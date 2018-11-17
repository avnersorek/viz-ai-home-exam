class VizException(Exception):
  def __init__(self, message, status_code):
      Exception.__init__(self)
      self.message = message
      self.status_code = status_code


class NoFacesException(VizException):
    def __init__(self):
        VizException.__init__(self,
            'No faces were detected',
            400
        )


class NoCommonFace(VizException):
    def __init__(self):
        VizException.__init__(self,
            'No common face was found',
            400
        )


class MustUploadImagesException(VizException):
    def __init__(self):
        VizException.__init__(self,
            'Must upload at least 2 images',
            400
        )
