# ARC_26_02 — Assignment 1: Forensic BIM

**Course:** DTU 41934 Advanced BIM  
**Group:** 2  
**Focus area:** Architecture — windows and natural light  
**Assignment:** [A1: Forensic BIM](https://timmcginley.github.io/41934/Assignments/A1.html)

## Project claim

> The existing Building 308 has a total floor area of 4,557.6 m², as stated in Section 2.3 of Team 26-06's client report.

The purpose of the investigation is to determine whether this value can be reproduced from the IFC model, [B308X.ifc](model/B308X.ifc).

Floor area is relevant to our focus area because it can later be compared with window area when assessing the relationship between windows and the spaces they serve. This investigation only considers the floor-area claim. It does not assess daylight performance.

## Research question

Can the reported floor area of 4,557.6 m² be reproduced from the area quantities stored in the IFC model?

A direct comparison is only meaningful if the client report and IFC use the same area definition. The report refers to a total floor area, but it does not clearly state whether this means net or gross floor area. The script therefore keeps these definitions separate.

## Method

The script in [main.py](main.py) opens the IFC model with IfcOpenShell and identifies all `IfcBuildingStorey` and `IfcSpace` entities.

For each space, the script:

1. Finds the building storey containing the space through its `Decomposes` relationship.
2. Follows `IfcRelDefinesByProperties` to find attached quantity sets.
3. Reads area values stored as `IfcQuantityArea` inside an `IfcElementQuantity`.
4. Prints the quantity-set name, area name and value for each space.
5. Adds `NetFloorArea` and `GrossFloorArea` to separate totals.
6. Checks whether every modelled space contains the area quantity used in the comparison.

The script does not add all area quantities together. Net floor area and gross floor area describe different measurements and cannot be combined into one total.

## IFC concepts used

| IFC concept | Use in the investigation |
| --- | --- |
| `IfcSpace` | Represents the spatial areas for which floor-area quantities are inspected. |
| `IfcBuildingStorey` | Identifies the storey to which each space belongs. |
| `IfcRelAggregates` / `Decomposes` | Connects an `IfcSpace` to its building storey. |
| `IfcRelDefinesByProperties` | Connects a space to its quantity information. |
| `IfcElementQuantity` | Contains the measured quantities attached to a space. |
| `IfcQuantityArea` | Stores area values such as `NetFloorArea` and `GrossFloorArea`. |

## Results

The IFC model contains six building storeys and three `IfcSpace` entities. All three spaces contain both `NetFloorArea` and `GrossFloorArea` quantities.

| Area definition | IFC total (m²) | Reported area (m²) | Difference (m²) | Difference (%) |
| --- | ---: | ---: | ---: | ---: |
| `NetFloorArea` | 4,683.81 | 4,557.60 | +126.21 | +2.77% |
| `GrossFloorArea` | 5,585.27 | 4,557.60 | +1,027.67 | +22.55% |

Neither IFC total reproduces the reported value of 4,557.6 m².

The net total is the closer result, but this does not prove that the reported value is incorrect. The report does not specify whether its value is net or gross, which floors and areas are included, or whether the same model revision was used.

## Identified issues

| Perspective | Finding |
| --- | --- |
| Design / reporting | The term “total floor area” is not defined clearly enough to support a like-for-like comparison. The report should state the area definition, calculation method and included building scope. |
| Modelling | The model contains only three `IfcSpace` entities across six storeys. These spaces may represent large floor zones rather than individual rooms. Their coverage should therefore be checked against the scope used in the report. |
| Tools | Counting spaces does not test a floor-area claim. The calculation must inspect the stored area quantities and keep net and gross values separate. The script now does this, but it relies on the quantities available in the IFC and does not independently calculate area from geometry. |

## Possible solutions

### Design / reporting

State whether the reported value is net or gross floor area. The report should also identify the calculation method, included storeys, exclusions and model revision.

### Modelling

Check whether the three modelled spaces cover the same parts of the building as the report. If the spatial coverage or quantities are incomplete, the spaces and their quantity information should be corrected before the comparison is repeated.

### Tools

Keep the current quantity-based check and add further analysis only where it supports the investigation. A geometry-based calculation could be considered later, but only if its assumptions and area definition can be explained clearly.

## Final verification status

**The claim cannot be reliably verified from the available information.**

The IFC `NetFloorArea` totals 4,683.81 m², which is 126.21 m² or 2.77% above the client-report value. The `GrossFloorArea` total differs by 1,027.67 m² or 22.55%.

The IFC therefore does not numerically reproduce the claim. However, the report's area definition and building scope are unclear, so the result cannot yet be described as a direct contradiction. A reliable conclusion requires confirmation that the report and IFC measure the same area using the same definition.