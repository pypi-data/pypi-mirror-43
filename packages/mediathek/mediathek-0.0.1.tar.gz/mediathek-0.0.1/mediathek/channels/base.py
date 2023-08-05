class BaseChannel:
    def all_videos(self):
        raise NotImplementedError

    def video(self, id):
        raise NotImplementedError

    def all_brands(self):
        raise NotImplementedError

    def brand(self):
        raise NotImplementedError
