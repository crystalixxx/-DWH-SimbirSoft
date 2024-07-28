from utils.download.download import DownloadFile
from utils.parse import Parser
from utils.prepare.converter import Converter

if __name__ == '__main__':
    DownloadFile.download()
    columns, rows = Parser.parse()

    main = Converter(columns, rows)
    main.validate_types()

