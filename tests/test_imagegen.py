"""Tests for webapp/imagegen.py — prompt enrichment and caching."""

import hashlib

from imagegen import (
    _extract_visual_details,
    _prompt_hash,
    enrich_prompt,
    get_cached_image,
    get_style_presets,
)

# ── get_style_presets ────────────────────────────────────────────────────────

class TestStylePresets:
    def test_returns_dict(self):
        presets = get_style_presets()
        assert isinstance(presets, dict)

    def test_has_default(self):
        presets = get_style_presets()
        assert "default" in presets

    def test_has_photorealistic(self):
        presets = get_style_presets()
        assert "photorealistic" in presets

    def test_preset_has_label(self):
        presets = get_style_presets()
        for key, val in presets.items():
            assert "label" in val, f"Preset '{key}' missing label"


# ── _prompt_hash ─────────────────────────────────────────────────────────────

class TestPromptHash:
    def test_deterministic(self):
        assert _prompt_hash("hello") == _prompt_hash("hello")

    def test_length(self):
        assert len(_prompt_hash("anything")) == 16

    def test_different_inputs(self):
        assert _prompt_hash("a") != _prompt_hash("b")

    def test_matches_sha256(self):
        expected = hashlib.sha256("test prompt".encode()).hexdigest()[:16]
        assert _prompt_hash("test prompt") == expected


# ── _extract_visual_details ──────────────────────────────────────────────────

class TestExtractVisualDetails:
    def test_extracts_appearance(self):
        desc = "A tall warrior in heavy armor. The sky was clear."
        result = _extract_visual_details(desc)
        assert "armor" in result.lower()

    def test_ignores_non_visual(self):
        desc = "He was thinking about philosophy. She felt sad."
        result = _extract_visual_details(desc)
        assert result == "" or result is None

    def test_truncates_long_output(self):
        desc = ". ".join(
            f"The character has elaborate clothing detail number {i} with intricate hair patterns"
            for i in range(50)
        )
        result = _extract_visual_details(desc)
        assert result is not None
        assert len(result) <= 300

    def test_max_four_sentences(self):
        desc = ". ".join(
            f"Detail {i} about their clothing and appearance"
            for i in range(10)
        )
        result = _extract_visual_details(desc)
        if result:
            # At most 4 sentences joined by ". "
            assert result.count(". ") <= 3


# ── enrich_prompt ────────────────────────────────────────────────────────────

class TestEnrichPrompt:
    def test_basic_subject_only(self):
        result = enrich_prompt("A medieval knight")
        assert "A medieval knight" in result

    def test_default_style_suffix(self):
        result = enrich_prompt("A castle", style="default")
        assert "high quality" in result

    def test_photorealistic_suffix(self):
        result = enrich_prompt("A castle", style="photorealistic")
        assert "cinematic lighting" in result

    def test_anime_prefix(self):
        result = enrich_prompt("A warrior", style="anime")
        assert "anime style" in result

    def test_genre_hint_fantasy(self):
        result = enrich_prompt("A sword", project_config={"genre": "fantasy"})
        assert "fantasy setting" in result

    def test_genre_hint_scifi(self):
        result = enrich_prompt("A ship", project_config={"genre": "scifi"})
        assert "sci-fi" in result

    def test_unknown_style_falls_back(self):
        result = enrich_prompt("A thing", style="nonexistent")
        # Should fall back to default preset
        assert "high quality" in result

    def test_with_entity_meta(self):
        meta = {
            "descriptions": {
                "machine": "Tall warrior wearing elaborate dark leather armor with silver buckles."
            }
        }
        result = enrich_prompt("A warrior", entity_meta=meta)
        assert "armor" in result.lower() or "leather" in result.lower()

    def test_strips_whitespace(self):
        result = enrich_prompt("  A castle  ")
        assert result.startswith("A castle")


# ── get_cached_image ─────────────────────────────────────────────────────────

class TestGetCachedImage:
    def test_cache_miss(self, tmp_path):
        cache_dir = tmp_path / "output" / "images"
        cache_dir.mkdir(parents=True)
        result = get_cached_image(tmp_path, "test-entity", "some prompt")
        assert result is None

    def test_cache_hit(self, tmp_path):
        cache_dir = tmp_path / "output" / "images"
        cache_dir.mkdir(parents=True)
        prompt = "a specific prompt"
        phash = hashlib.sha256(prompt.encode()).hexdigest()[:16]
        filename = f"test-entity_{phash}.png"
        (cache_dir / filename).write_text("fake image")
        result = get_cached_image(tmp_path, "test-entity", prompt)
        assert result == filename
