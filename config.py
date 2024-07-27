class Settings:
    DOWNLOAD_URL = "https://cloud.mail.ru/public/L1xB/nvgHGYJz5"
    CURRENT_FILE_NAME = "testfile"
    CURRENT_FILE_EXTENSION = "csv"  # only csv or json

    @staticmethod
    def get_file_path() -> str:
        return Settings.CURRENT_FILE_NAME + '.' + Settings.CURRENT_FILE_EXTENSION


settings = Settings()
