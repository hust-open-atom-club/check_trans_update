from pathlib import Path
from build_site import Commit, parse_todolist
from build_site import render_needs_translation, render_needs_update

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
    skipped_paths = [lines[0] for lines in result.skipped]
    assert "Documentation/weird/broken.rst" in skipped_paths
    assert "Documentation/translations/zh_CN/fake/only-merges.rst" in skipped_paths
    assert len(result.skipped) == 2


def test_render_needs_translation_lists_paths():
    result = parse_todolist(FIXTURE.read_text())
    md = render_needs_translation(result.needs_translation)
    assert md.startswith("# Needs translation")
    assert "Documentation/w1/w1-netlink.rst" in md
    assert "Documentation/RCU/rcubarrier.rst" in md
    assert "2 file" in md  # count header


def test_render_needs_update_shows_commits():
    result = parse_todolist(FIXTURE.read_text())
    md = render_needs_update(result.needs_update)
    assert md.startswith("# Needs update")
    assert "Documentation/translations/zh_CN/subsystem-apis.rst" in md
    assert "002ec8f1c69d" in md
    assert "Documentation: Fix typos" in md
    assert "2 file" in md


def test_main_writes_two_markdown_files(tmp_path):
    from build_site import main

    todo = tmp_path / "TODO_LIST"
    todo.write_text(FIXTURE.read_text())
    out = tmp_path / "docs"
    out.mkdir()

    main(["--todo", str(todo), "--out", str(out)])

    assert (out / "needs-translation.md").exists()
    assert (out / "needs-update.md").exists()
    assert "w1-netlink" in (out / "needs-translation.md").read_text()
    assert "002ec8f1c69d" in (out / "needs-update.md").read_text()
