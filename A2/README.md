# A2 - Daylight checks and window-sizing support

**Course:** 41934 Advanced BIM  
**Group:** 10

We will extend Group 10's daylight-checking workflow from 2025. Our aim is to show how much glazing a room lacks, which rooms need attention, and how proposed changes affect the result.

## A2a - Group and focus

- **Python confidence:** 3
- **Focus area:** Indoor and Energy - daylight

## A2b - Claim and starting point

**Building:** Building \#2508

We will check whether the relevant rooms meet the area requirement under the BR18 10% method. If the report has no explicit claim about this method, we will describe it as an issue to investigate.

### Group 10's work

Group 10's README proposes a corrected glazing-area check, accounting for light transmittance, shading, wall thickness, room depth and other relevant factors. They also propose a Blender interface for reviewing rooms during design.

The version we have examined outputs storey, room name, floor area, window area, ratio and window count. Their README describes their intended functionality; it does not establish which correction factors were implemented. We will review the code before deciding what can be reused.

Our contribution is to turn these checks into quantities for design decisions: glazing deficits, margins, review priorities and window-size scenarios. Corrected glazing and design-stage feedback are already part of Group 10's proposal.

### Basis of the check

BR18 §379 allows daylight provision to be documented using the 10% method. This uses glass area with applicable corrections and the relevant floor area for the room use. We must therefore confirm what the existing area values represent.

An uncorrected window-area ratio will be labelled as a preliminary check. Missing glass areas, correction inputs or room-use information will be reported. We will not treat an assumed value as verified model data. Any applicable residential provisions must be checked before drawing a regulatory conclusion.

## A2c - Use case

- **Use case:** Daylight review with window-sizing support
- **Closest BIM use cases:** Code Validation and Design Review
- **BIM purposes:** Gather, analyse and communicate
- **Phase:** Design, before window sizes are fixed and after changes to rooms, windows or shading

The architect provides the IFC model and confirms room uses and assumptions. The BIM analyst checks the data and runs the tool. The BIM coordinator reviews the results with the architect, who assesses changes and updates the model.

### Workflow

1. Receive the IFC model, report claim and supplementary inputs.
2. Identify relevant rooms and their associated windows.
3. Validate areas, units and correction inputs. Return unresolved issues to the model author.
4. Calculate ratios, glazing deficits and margins.
5. Rank rooms for review and compare proposed window changes.
6. Export the results, review the design and repeat after model revisions.

[SVG](A2\IMG\BPMN.svg)

## A2d - Scope

We will reuse reliable parts of the existing extraction and add data checks, derived measures, scenario comparisons and reporting. The first version will not modify the IFC model or generate geometry.

Full daylight simulation, automatic geometric shading calculations, energy use, overheating, glare and cost calculations are outside this scope. They need information and methods beyond the existing area outputs.

## A2e - Tool idea

The Python/IfcOpenShell tool will produce a room table and storey summary. Each room will retain its IFC GUID so findings can be traced back to the model.

Let `A_f` be the relevant floor area and `A_g` the corrected equivalent glass area, both in m². Corrections must follow the adopted BR18 guidance.

| Measure | Calculation |
| --- | --- |
| Glazing ratio (%) | `100 × A_g / A_f` |
| Required corrected glass area (m²) | `0.10 × A_f` |
| Area margin (m²) | `A_g − 0.10 × A_f` |
| Glazing deficit (m²) | `max(0, 0.10 × A_f − A_g)` |
| Ratio margin (percentage points) | `100 × A_g / A_f − 10` |
| Floor area supported at the threshold (m²) | `A_g / 0.10` |

For example, a room with 30 m² of relevant floor area and 2.4 m² of corrected glass area has an 8% ratio and a 0.6 m² deficit. This is an illustrative calculation, not a model result.

The deficit refers to corrected equivalent glass area. Additional physical glazing must be assessed using its own properties and corrections.

### Scenarios and priorities

Users can enter a proposed window enlargement, replacement or additional window and compare its result with the baseline. The tool will show the revised ratio and remaining deficit without changing the model. These scenarios do not establish whether a change is physically feasible.

Rooms below the threshold will be ranked by glazing deficit, with ratio margins alongside. Missing-data cases will be listed separately. Storey summaries will show room counts, rooms below the threshold, unassessable rooms and total room-level deficits. Surpluses will not cancel deficits in other rooms.

### Value and validation

The tool reduces repeated calculations and gives the design team specific quantities to act on. Visible assumptions and room identifiers make the findings easier to review and track after revisions. This supports better-informed decisions about daylight in occupied spaces.

We will compare selected model quantities and results with manual checks. Validation will cover rooms below, at and above the threshold, missing data, invalid areas, unit conversion and ambiguous window associations. Scenario calculations will also be checked manually.

## A2f - Information requirements

These are candidate sources. Their availability must be checked in the selected IFC model.

| Information | IFC source or supplementary input |
| --- | --- |
| Room identifier and name | `IfcSpace.GlobalId`, `Name`, `LongName` |
| Storey | `IfcBuildingStorey` and spatial relationships such as `IfcRelAggregates` |
| Room use and relevant floor area | Space properties, reviewed room schedule and `Qto_SpaceBaseQuantities.NetFloorArea` where appropriate |
| Window identifier and dimensions | `IfcWindow.GlobalId`, `OverallWidth`, `OverallHeight` and available quantities |
| Actual glass area | Verified quantities or glazing schedule; overall window dimensions are not sufficient by themselves |
| Window-to-room association | Suitable `IfcRelSpaceBoundary` relationships or an explicit GUID mapping |
| Transmittance and correction inputs | Verified model properties and supplementary correction records |
| Units | `IfcProject.UnitsInContext` |

We plan to retrieve entities with `ifc.by_type()` and inspect properties and quantities using IfcOpenShell utilities.

## A2g - Licence

Group 10 of 2025's README states that they chose GPL 3.0. We propose GPL 3.0 for an extension that includes their GPL-covered code, subject to checking the repository's actual licence terms. We will retain the required attribution and licence notices.

## References

- [41934 Advanced BIM — A2: Use Case](https://timmcginley.github.io/41934/Assignments/A2.html)
- [Group 10 — original repository](https://github.com/kinolaj/ABIM_group10) — output description supplied by our group; code and licence review pending.
- [BR18 — Dagslys, §§379–381](https://www.bygningsreglementet.dk/tekniske-bestemmelser/18/krav/379_381/)
- [BR18 — Daylight guidance](https://www.bygningsreglementet.dk/tekniske-bestemmelser/18/vejledninger/generel_vejledning/dagslys/)
- [BR18 — Corrections to the 10% rule](https://www.bygningsreglementet.dk/tekniske-bestemmelser/18/vejledninger/10-procent-vejledning/)
