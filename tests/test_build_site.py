from pathlib import Path
from build_site import parse_todolist

FIXTURE = Path(__file__).parent / "fixtures" / "todo_list_sample.txt"


def test_parse_identifies_needs_translation_records():
    result = parse_todolist(FIXTURE.read_text())
    paths = [r.path for r in result.needs_translation]
    assert paths == [
        "Documentation/w1/w1-netlink.rst",
        "Documentation/RCU/rcubarrier.rst",
    ]
