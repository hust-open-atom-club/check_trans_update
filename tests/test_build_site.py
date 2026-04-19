from pathlib import Path
from build_site import Commit, parse_todolist

FIXTURE = Path(__file__).parent / "fixtures" / "todo_list_sample.txt"


def test_parse_identifies_needs_translation_records():
    result = parse_todolist(FIXTURE.read_text())
    paths = [r.path for r in result.needs_translation]
    assert paths == [
        "Documentation/w1/w1-netlink.rst",
        "Documentation/RCU/rcubarrier.rst",
    ]


def test_parse_identifies_needs_update_records():
    result = parse_todolist(FIXTURE.read_text())
    assert len(result.needs_update) == 2

    subsystem = result.needs_update[0]
    assert subsystem.path == "Documentation/translations/zh_CN/subsystem-apis.rst"
    assert subsystem.total == 1
    assert subsystem.commits == [
        Commit(
            sha="002ec8f1c69d",
            subject="Documentation: Document the NVMe PCI endpoint target driver",
        )
    ]

    energy = result.needs_update[1]
    assert energy.total == 2
    assert [c.sha for c in energy.commits] == ["eb1ad4d43167", "d56b699d76d1"]


def test_parse_skips_unrecognized_records():
    result = parse_todolist(FIXTURE.read_text())
    assert len(result.skipped) == 1
    assert result.skipped[0][0] == "Documentation/weird/broken.rst"
