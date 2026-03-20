# Procedural History Generation — The Shattered Crown
## Task: Generate 50 years of history

## World State

Genre: fantasy
Calendar: Reckoning of Ages

Eras: Age of Dawn (1A), Age of Crowns (2A)

### Species (3)
- Stonewarden: sapient, pop ~~150,000
- Eldari: sapient, pop ~~80,000
- Human: sapient, pop ~~2 million

### Factions (1)
- The Silver Order: active
  Goals: Protect Valdris, Guard the Weave Gates, Maintain peace

### Locations (2)
- Valdris [city]: pop ~50,000
- The Sunken Library [ruins]: pop ~200 (scholars and guardians)

### Resources (7)
- Iron [raw-material]: common
- Timber [raw-material]: common
- Grain [food]: abundant
- Weave Fragments [magical]: very-rare
- Ancient Texts [knowledge]: rare
- Stonewarden Steel [strategic]: uncommon
- Horses [strategic]: common

### Existing Timeline (last 5 events)
- [1A 487] The Sundering (cataclysm)
- [2A 12] Founding of Valdris (founding)
- [7 Stormfall, 2A 215] Birth of Kael Dawnblade (birth)
- [2A 230] The War of Broken Crowns (war)
- [3 Ashfall, 2A 237] Death of Queen Morwen (death)

### World Constraints

## Generation Instructions
Generate 50 years of history for this world.
Output as a sequence of event YAML frontmatter blocks.

Focus on: wars, rebellions, sieges, betrayals, power struggles, resource conflicts.

For each event, output:
```yaml
---
name: "Event Name"
type: war|battle|birth|death|founding|discovery|plague|cataclysm|trade_agreement|coronation|rebellion|treaty|milestone
date: "ERA YEAR"                    # or start_date/end_date for duration events
significance: trivial|minor|moderate|major|world-changing
scope: personal|local|regional|national|continental|global
participants:
  - entity: "entity-slug"
    role: "description"
locations: ["location-slug"]
caused_by: ["previous-event-slug"]
leads_to: ["next-event-slug"]
economic_impact:
  production_effects: []
  trade_effects: []
---
Brief description of the event and its consequences.
```

Rules:
- Events must be chronologically ordered
- Causality chains must be logical (cause precedes effect)
- Respect ALL world flags (no gunpowder tech if flag is false, etc.)
- Dead characters cannot participate in later events
- Reference existing entities by their slugs
- You may create NEW entities (characters, factions, locations) as needed
- Economic impacts should cascade realistically
