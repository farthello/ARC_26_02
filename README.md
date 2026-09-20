# ARC_26_02 — Assignment 1: Forensic BIM

Course: 41934 Advanced BIM. [Assignment 1 brief](https://timmcginley.github.io/41934/Assignments/A1.html).

## Group number

Group 2.

## Focus area

Architecture — windows and natural light.

Our selected investigation concerns the definition and reproducibility of floor area. A consistent area definition is relevant when relating window area to floor area in an architectural assessment; this investigation does not yet evaluate daylight performance.

## Selected claim and source

- **Report:** Existing Building Report, Team 26 06.
- **Location:** Section 2.3.
- **Claim to investigate:** The reported floor area of the existing building.
- **Model available in this repository:** [B308X.ifc](model/B308X.ifc).

The report reference comes from our initial project notes. The exact area value, unit, and wording still need to be recorded from Section 2.3 before completing a numerical comparison. We also need to confirm that the model and report describe the same building scope and revision.

## Identified issue and possible causes

Our initial review identified that the reported floor area could not be directly reproduced from the IFC model. The notes indicate that the report does not specify whether the figure is gross or net floor area, or which calculation standard was used. Without a shared definition and scope, the reported and model-derived values cannot be reliably compared.

| Perspective | Assessment |
| --- | --- |
| Design / reporting | The primary issue identified in our notes is an unclear area definition in the report. This limits verification of the analysis; it does not establish an error in the physical design. |
| Modelling | Missing or inconsistent space boundaries, area quantities, or storey coverage could affect an area total. These are possible causes to investigate, not confirmed model defects. |
| Tools | A calculation could select the wrong quantities or combine values with different definitions or units. The current scripts count spaces and do not yet check floor area. No defect in IfcOpenShell has been established. |

## Possible solutions

### Design / reporting

State whether the reported area is gross or net, identify the calculation standard, and describe the included floors and any exclusions. Present the value and unit alongside this method so another person can reproduce the result.

### Modelling

Check that the relevant spaces and storeys cover the scope of the report. Inspect their boundaries and available area quantities. Where information is missing or inconsistent, propose corrections and record the area definition used before recalculating totals.

### Tools

Extend the IfcOpenShell script to inspect available area quantities and extract those matching the agreed definition. Report each contributing element's identifier, storey, quantity name, value, and unit. Flag missing quantities rather than treating them as zero, and compare the resulting total with the report using an explicitly stated tolerance.

## Verification status and next steps

[main.py](main.py) currently opens the IFC model and counts `IfcSpace` entities. The configured requirement of 21 spaces is a separate check and does not verify the floor-area claim. A text inspection of the IFC file found three `IFCSPACE` records; this alone does not establish whether the model's spatial coverage is complete.

To complete the investigation:

1. Record the exact reported area and unit from Section 2.3 and confirm its definition and scope.
2. Inspect the corresponding model quantities, units, and spatial coverage.
3. Implement and run the area comparison, documenting assumptions and any missing data.
4. Record whether the claim is supported, contradicted, or cannot be verified with the available information.

**Current conclusion:** The floor-area claim remains unverified. The available work identifies a reproducibility concern but does not demonstrate a numerical discrepancy.

## Submission checklist

The [Assignment 1 brief](https://timmcginley.github.io/41934/Assignments/A1.html) also requires issue logging and submission through the course channels:

- [ ] Log the issue in the course Google form.
- [ ] Ensure the submitted GitHub repository is public and contains the updated README.
- [ ] Submit a `.txt` file containing the repository link to DTU Learn.
