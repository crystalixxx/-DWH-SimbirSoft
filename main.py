from utils.download.download import DownloadFile
from utils.parse import Parser


if __name__ == '__main__':
    DownloadFile.download()
    columns, rows = Parser.parse()

