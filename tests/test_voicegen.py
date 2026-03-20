"""Tests for webapp/voicegen.py — voice instruct building and caching."""

import hashlib

from voicegen import build_voice_instruct, get_cached_voice

# ── build_voice_instruct ─────────────────────────────────────────────────────

class TestBuildVoiceInstruct:
    def test_manual_override(self):
        voice = {"instruct": "A gruff old pirate voice"}
        result = build_voice_instruct(voice, {})
        assert result == "A gruff old pirate voice"

    def test_manual_override_takes_precedence(self):
        voice = {"instruct": "override", "description": "ignored", "accent": "ignored"}
        result = build_voice_instruct(voice, {"gender": "male", "age": "30"})
        assert result == "override"

    def test_gender_male(self):
        result = build_voice_instruct({}, {"gender": "male"})
        assert "male" in result

    def test_gender_female(self):
        result = build_voice_instruct({}, {"gender": "female"})
        assert "female" in result

    def test_gender_shorthand(self):
        assert "male" in build_voice_instruct({}, {"gender": "m"})
        assert "female" in build_voice_instruct({}, {"gender": "f"})
        assert "male" in build_voice_instruct({}, {"gender": "man"})
        assert "female" in build_voice_instruct({}, {"gender": "woman"})

    def test_age_teenage(self):
        result = build_voice_instruct({}, {"age": "17"})
        assert "teenage" in result

    def test_age_young_adult(self):
        result = build_voice_instruct({}, {"age": "25"})
        assert "young adult" in result

    def test_age_middle_aged(self):
        result = build_voice_instruct({}, {"age": "45"})
        assert "middle-aged" in result

    def test_age_mature(self):
        result = build_voice_instruct({}, {"age": "55"})
        assert "mature" in result

    def test_age_elderly(self):
        result = build_voice_instruct({}, {"age": "71"})
        assert "elderly" in result

    def test_age_with_text(self):
        # "34 (at start of story)" should parse as 34
        result = build_voice_instruct({}, {"age": "34 (at start of story)"})
        assert "young adult" in result

    def test_description_included(self):
        voice = {"description": "Deep, resonant, with a slight rasp"}
        result = build_voice_instruct(voice, {})
        assert "Deep, resonant" in result

    def test_tags_included(self):
        voice = {"tags": ["male", "deep", "warm", "slow"]}
        result = build_voice_instruct(voice, {"gender": "male"})
        # "male" tag should be filtered out, others included
        assert "deep" in result
        assert "warm" in result

    def test_tags_filter_gender(self):
        voice = {"tags": ["female", "soft", "calm"]}
        result = build_voice_instruct(voice, {})
        qualities_part = [p for p in result.split(". ") if "Voice qualities" in p]
        if qualities_part:
            assert "female" not in qualities_part[0]

    def test_accent_from_character(self):
        voice = {"accent": "Scottish"}
        result = build_voice_instruct(voice, {})
        assert "Scottish" in result

    def test_accent_from_location_fallback(self):
        location = {
            "regional_defaults": {
                "voice": {"accent": "West Country", "dialect": "rural"}
            }
        }
        result = build_voice_instruct({}, {}, location)
        assert "West Country" in result

    def test_character_accent_overrides_location(self):
        voice = {"accent": "Cockney"}
        location = {
            "regional_defaults": {
                "voice": {"accent": "West Country"}
            }
        }
        result = build_voice_instruct(voice, {}, location)
        assert "Cockney" in result
        assert "West Country" not in result

    def test_dialect_included(self):
        voice = {"dialect": "formal court speech"}
        result = build_voice_instruct(voice, {})
        assert "formal court speech" in result

    def test_empty_inputs_fallback(self):
        result = build_voice_instruct({}, {})
        assert result == "A neutral, clear speaking voice."

    def test_full_character(self):
        voice = {
            "description": "Thin, reedy, slow",
            "tags": ["male", "old", "thin", "slow"],
            "accent": "soft rural English",
            "dialect": "formal village speech",
        }
        meta = {"gender": "male", "age": "71"}
        result = build_voice_instruct(voice, meta)
        assert "male" in result
        assert "elderly" in result
        assert "Thin, reedy, slow" in result
        assert "soft rural English" in result
        assert "formal village speech" in result


# ── get_cached_voice ─────────────────────────────────────────────────────────

class TestGetCachedVoice:
    def test_cache_miss(self, tmp_path):
        voices_dir = tmp_path / "output" / "voices"
        voices_dir.mkdir(parents=True)
        result = get_cached_voice(tmp_path, "test-char", "hello world", "A deep voice")
        assert result is None

    def test_cache_hit(self, tmp_path):
        voices_dir = tmp_path / "output" / "voices"
        voices_dir.mkdir(parents=True)
        slug = "test-char"
        text = "hello world"
        instruct = "A deep voice"
        cache_key = hashlib.sha256(f"{slug}:{instruct}:{text}".encode()).hexdigest()[:16]
        filename = f"{slug}_{cache_key}.mp3"
        (voices_dir / filename).write_text("fake audio")
        result = get_cached_voice(tmp_path, slug, text, instruct)
        assert result == filename
