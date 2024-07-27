from utils.url import UrlHandler


class Settings:
    def __init__(self, url: str, resource: str, file_name: str, file_extension: str):
        self.__url = url
        self.__resource = resource
        self.__file_name = file_name
        self.__file_extension = file_extension

        handler = UrlHandler(self.__url, self.__resource)

        try:
            self.__url = handler.hande_url()
        except ValueError as e:
            pass

    def get_file_path(self) -> str:
        return self.__file_name + '.' + self.__file_extension

    def get_url(self) -> str:
        return self.__url


settings = Settings("https://cloud.mail.ru/public/L1xB/nvgHGYJz5", "mail",
                    "testfile", "csv")
