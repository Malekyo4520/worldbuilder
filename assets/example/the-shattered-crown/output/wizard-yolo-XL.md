# 🧙 World Creation Wizard — Extra Large — Epic Universe / Sandbox

## Mode: YOLO (Full Auto-Generation)

Genre: **fantasy**
Size: **XL** — Extra Large — Epic Universe / Sandbox
Tone: **epic**
Type: **novel**
Seed: **test**


## Generation Targets

Size **XL** means generating within these ranges:

| Entity Type     | Min | Max |
|-----------------|-----|-----|
| species         |   8 |  20 |
| races           |  12 |  40 |
| languages       |   8 |  25 |
| characters      |  40 | 100 |
| locations       |  25 |  80 |
| factions        |   8 |  25 |
| items           |  10 |  30 |
| events          |  50 | 200 |
| lineages        |   5 |  15 |
| arcs            |   5 |  15 |
| magic_systems   |   2 |   5 |

| History         |     |     |
| Eras            |   4 |   8 |
| History (years) | 5000 | 50000 |
| Gen passes      |   5 |     |

| Economy         |     |     |
| currencies      |   3 |  10 |
| resources       |  12 |  40 |
| trade_routes    |   5 |  25 |


## Generation Instructions

Generate a complete fantasy world for a novel with epic tone.
Creative seed: "test"

Generate ALL entities within the ranges above. For each entity, output valid
YAML frontmatter + Markdown body matching the WorldBuilder schemas.

**Generation order:**
1. Calendar & eras
2. World flags (technology, magic, social rules)
3. Species & races
4. Languages & language families
5. Geography (locations, spatial hierarchy, routes)
6. Factions & organizations
7. Lineages & dynasties
8. Economy (currencies, resources, production, trade routes)
9. Characters (with full family_links, triple descriptions)
10. Historical events (causality chains, 5 passes)
11. Story arcs
12. Items of significance
13. Magic systems (if applicable)

**After each generation pass:**
Run ALL validation editors in order: worldrules, continuity, geography, characterization, lore, sensitivity
Fix any issues before proceeding to the next entity type.

## Output Format

For each entity, output as a separate file block:

```
=== FILE: world/{entity_type}/{slug}.md ===
---
(YAML frontmatter matching the entity schema)
---

(Markdown body with descriptions, notes, etc.)
```

Entity filenames must be kebab-case slugs.
All cross-references must use slugs that match actual generated entities.
Relationships must be bidirectional (if A references B, B must reference A).

After all entities are generated, output:
1. `project.yaml` with all settings, style, and world_flags
2. `world/calendar.yaml` with eras and months
3. `world/economy.yaml` with full economic data

## Post-Generation Validation

After ALL entities are generated, run these validation checks:

| Pass | Editor          | Checks                                          |
|------|-----------------|--------------------------------------------------|
| 1    | worldrules      | World flag compliance, tech anachronisms          |
| 2    | geography       | Spatial hierarchy, route validity, terrain logic   |
| 3    | continuity      | Timeline order, causality chains, alive/dead       |
| 4    | lore            | Internal consistency, cross-references valid        |
| 5    | characterization| Voice consistency, trait alignment, relationships  |
| 6    | sensitivity     | Content rating compliance, appropriateness         |

On failure: fix the issue and re-validate. Max 3 retries per entity.
Flag unresolvable issues for human review.
