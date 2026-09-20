# ARC_26_02 — Assignment 1: Forensic BIM

Course: 41934 Advanced BIM. [Assignment 1 brief](https://timmcginley.github.io/41934/Assignments/A1.html).

## Group number

Group 2.

## Focus area

Architecture — windows and natural light.

For this investigation, we are looking at the floor area of the existing building and whether the value stated in the client report can be reproduced from the IFC model.

Floor area is relevant to our focus area because it can later be compared with window area when assessing the relationship between windows and the spaces they serve. At this stage, we are only investigating the floor area and not the daylight performance itself.

## Selected claim and source

- **Report:** Existing Building Report, Team 26 06
- **Location:** Section 2.3
- **Claim:** Reported floor area of the existing building
- **IFC model:** [B308X.ifc](model/B308X.ifc)

Before making a numerical comparison, we need to confirm the exact area stated in Section 2.3, including the unit and how the area has been defined. We also need to make sure that the report and IFC model cover the same parts and revision of the building.

## Identified issue and possible causes

From our initial review, the reported floor area cannot be directly reproduced from the IFC model.

One issue is that it is not clear whether the reported value refers to gross or net floor area, or which method has been used to calculate it. Without the same definition and building scope, comparing the report directly with an IFC-derived value could give a misleading result.

| Perspective | Assessment |
| --- | --- |
| Design / reporting | The report does not clearly define how the floor area has been calculated. This makes the stated value difficult to verify, but does not necessarily mean that the value itself is incorrect. |
| Modelling | Missing or inconsistent space boundaries, area quantities or storey coverage could affect the calculated floor area. These need to be checked before concluding that there is an issue with the model. |
| Tools | The script needs to use quantities that match the agreed area definition. Using the wrong IFC quantities, units or elements could produce a different result even if the model itself is correct. |

## Possible solutions

### Design / reporting

The reported floor area should include a clear definition of what is being measured, for example gross or net floor area. The calculation method, included floors and any excluded areas should also be stated. This would make it possible to reproduce and verify the reported value.

### Modelling

The relevant `IfcSpace` entities and building storeys should be checked to see whether they represent the full scope used in the report. Their boundaries and available area quantities should also be inspected.

If information is missing or inconsistent, this should be documented before calculating the total area.

### Tools

The IfcOpenShell script can be extended to extract the available area quantities from the model.

For each area included in the calculation, the script should record:

- IFC identifier
- Storey
- Quantity name
- Area value
- Unit

Missing quantities should be flagged instead of being counted as zero. Once the area definition has been established, the calculated IFC area can be compared with the value from the client report.

## Verification status and next steps

The current [main.py](main.py) opens the IFC model and counts `IfcSpace` entities. The requirement of 21 spaces is a separate model check and does not verify the floor-area claim.

The IFC file currently contains three `IfcSpace` records. However, the number of spaces alone is not enough to determine whether the spatial coverage of the model is complete or whether the reported floor area can be reproduced.

The next steps are:

1. Record the exact floor area and unit stated in Section 2.3.
2. Determine how the reported floor area has been defined and which parts of the building are included.
3. Inspect the area quantities, units and spatial coverage available in the IFC model.
4. Extend the script to calculate the corresponding area from the IFC.
5. Compare the two values and document any assumptions or missing information.
6. Conclude whether the claim is supported, contradicted or cannot be verified from the available IFC information.

## Current conclusion

The reported floor area has not yet been verified from the IFC model. At this stage, the main issue is that the area definition and scope are not clear enough to make a reliable comparison.

