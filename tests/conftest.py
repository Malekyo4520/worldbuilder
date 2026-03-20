"""Shared fixtures for WorldBuilder tests."""

import sys
from pathlib import Path

import pytest

# Add project paths so we can import from scripts/ and webapp/
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "webapp"))


@pytest.fixture
def sample_entities():
    """Minimal entity collection for testing name indexing and ref resolution."""
    return {
        "character": {
            "rowan-thornfield": {
                "meta": {"name": "Rowan Thornfield", "species": "humans", "race": "valley-folk"},
                "body": "",
                "file": Path("world/characters/rowan-thornfield.md"),
            },
            "elda-greenhand": {
                "meta": {"name": "Elda Greenhand", "species": "humans", "faction": "aldfield-council"},
                "body": "",
                "file": Path("world/characters/elda-greenhand.md"),
            },
        },
        "faction": {
            "aldfield-council": {
                "meta": {"name": "Aldfield Village Council", "leader": "col-the-elder"},
                "body": "",
                "file": Path("world/factions/aldfield-council.md"),
            },
        },
        "species": {
            "humans": {
                "meta": {"name": "Humans", "races": ["valley-folk"]},
                "body": "",
                "file": Path("world/species/humans.md"),
            },
        },
    }


@pytest.fixture
def calendar_config():
    """Calendar config with two eras for date testing."""
    return {
        "eras": [
            {"name": "Age of Crowns", "prefix": "AC", "sort_order": 1},
            {"name": "The Quiet Years", "prefix": "QY", "sort_order": 2},
        ]
    }


@pytest.fixture
def tmp_project(tmp_path):
    """Create a minimal project directory structure for filesystem tests."""
    proj = tmp_path / "test-project"
    (proj / "world" / "characters").mkdir(parents=True)
    (proj / "world" / "locations").mkdir(parents=True)
    (proj / "output" / "images").mkdir(parents=True)
    (proj / "output" / "voices").mkdir(parents=True)

    # project.yaml
    (proj / "project.yaml").write_text(
        "title: Test Project\ngenre: fantasy\ntype: worldbook\n"
    )

    # A character entity
    (proj / "world" / "characters" / "test-hero.md").write_text(
        "---\nname: Test Hero\nrole: protagonist\nstatus: alive\nspecies: humans\n---\n\n## Notes\nA test character.\n"
    )

    return proj
