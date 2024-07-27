from utils.download import DownloadFile
from utils.parse_csv import Parser
from config import settings

if __name__ == '__main__':
    DownloadFile.download()
    columns, rows = Parser.parse()

    print(columns)
    print(rows)

