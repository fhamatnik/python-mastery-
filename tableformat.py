# tableformat.py

from abc import ABC, abstractmethod


class TableFormatter(ABC):
    @abstractmethod
    def headings(self, headers):
        raise NotImplementedError()

    @abstractmethod
    def row(self, rowdata):
        raise NotImplementedError()


class TextTableFormatter(TableFormatter):
    def headings(self, headers):
        print(" ".join("%10s" % h for h in headers))
        print(("-" * 10 + " ") * len(headers))

    def row(self, rowdata):
        print(" ".join("%10s" % d for d in rowdata))


class CSVTableFormatter(TableFormatter):
    def headings(self, headers):
        print(",".join(headers))

    def row(self, rowdata):
        print(",".join(map(str, rowdata)))


class HTMLTableFormatter(TableFormatter):
    @staticmethod
    def _tag(tag, content):
        return f"<{tag}>{content}</{tag}>"

    def headings(self, headers):
        print(self._tag("tr", " ".join(self._tag("th", h) for h in headers)))

    def row(self, rowdata):
        print(self._tag("tr", " ".join(self._tag("td", r) for r in rowdata)))


def create_formatter(kind):
    match kind:
        case "text":
            return TextTableFormatter()
        case "csv":
            return CSVTableFormatter()
        case "html":
            return HTMLTableFormatter()
        case _:
            raise ValueError(
                f"Unsupported formatter {kind}, must be one of text, csv, html"
            )


# Print a table
def print_table(records, fields, formatter):
    if not isinstance(formatter, TableFormatter):
        raise TypeError("Expected a TableFormatter")
    formatter.headings(fields)
    for r in records:
        rowdata = [getattr(r, fieldname) for fieldname in fields]
        formatter.row(rowdata)
