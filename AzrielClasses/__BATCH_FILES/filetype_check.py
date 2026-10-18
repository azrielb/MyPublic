import sys
import filetype


def detect(path):
    kind = filetype.guess(path)
    if kind is None:
        return "Unknown (not recognized by content)"
    return f"{kind.mime} (.{kind.extension})"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <file> [file...]")
        sys.exit(1)
    for p in sys.argv[1:]:
        try:
            print(f"{p}: {detect(p)}")
        except OSError as e:
            print(f"{p}: error - {e}")
