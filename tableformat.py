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


class ColumnFormatMixin:
    formats = []

    def row(self, rowdata):
        rowdata = [(fmt % d) for fmt, d in zip(self.formats, rowdata)]
        super().row(rowdata)


class UpperHeadersMixin:
    def headings(self, headers):
        super().headings([h.upper() for h in headers])


def create_formatter(kind, column_formats=[], upper_headers=False):
    match kind:
        case "text":
            formatter_cls = TextTableFormatter
        case "csv":
            formatter_cls = CSVTableFormatter
        case "html":
            formatter_cls = HTMLTableFormatter
        case _:
            raise ValueError(
                f"Unsupported formatter {kind}, must be one of text, csv, html"
            )

    if column_formats:

        class formatter_cls(ColumnFormatMixin, formatter_cls):
            formats = column_formats

    if upper_headers:

        class formatter_cls(UpperHeadersMixin, formatter_cls):
            pass

    return formatter_cls()


# Print a table
def print_table(records, fields, formatter):
    if not isinstance(formatter, TableFormatter):
        raise TypeError("Expected a TableFormatter")
    formatter.headings(fields)
    for r in records:
        rowdata = [getattr(r, fieldname) for fieldname in fields]
        formatter.row(rowdata)
