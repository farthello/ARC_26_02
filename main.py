import ifcopenshell 

# Client report claim
REPORTED_AREA = 4557.6  # m²


def get_storey(space):
    """Find the building storey containing an IfcSpace."""
    for relation in space.Decomposes:
        if relation.RelatingObject.is_a("IfcBuildingStorey"):
            return relation.RelatingObject

    return None


def get_area_quantities(space):
    """Find area quantities stored on an IfcSpace."""
    areas = []

    for relation in space.IsDefinedBy:
        if not relation.is_a("IfcRelDefinesByProperties"):
            continue

        quantity_set = relation.RelatingPropertyDefinition

        if not quantity_set.is_a("IfcElementQuantity"):
            continue

        for quantity in quantity_set.Quantities:
            if quantity.is_a("IfcQuantityArea"):
                areas.append({
                    "set": quantity_set.Name,
                    "name": quantity.Name,
                    "value": float(quantity.AreaValue),
                })

    return areas


def main():
    model = ifcopenshell.open("model/B308X.ifc")

    spaces = model.by_type("IfcSpace")
    storeys = model.by_type("IfcBuildingStorey")

    print("CLIENT CLAIM")
    print(f"Reported floor area: {REPORTED_AREA:.1f} m²")

    print("\nIFC MODEL")
    print(f"Building storeys: {len(storeys)}")
    print(f"IfcSpaces: {len(spaces)}")

    net_total = 0
    gross_total = 0

    net_count = 0
    gross_count = 0

    print("\nSPACE AREA QUANTITIES")

    for space in spaces:
        storey = get_storey(space)
        areas = get_area_quantities(space)

        storey_name = storey.Name if storey else "No storey"
        space_name = space.Name or "Unnamed"

        print(f"\n{space_name} | {storey_name}")

        if not areas:
            print("  No area quantity found")
            continue

        for area in areas:
            print(
                f"  {area['set']} / {area['name']}: "
                f"{area['value']:.2f} m²"
            )

            if area["name"] == "NetFloorArea":
                net_total += area["value"]
                net_count += 1

            elif area["name"] == "GrossFloorArea":
                gross_total += area["value"]
                gross_count += 1

    print("\nAREA TOTALS")

    if net_count:
        print(
            f"NetFloorArea: {net_total:.2f} m² "
            f"({net_count}/{len(spaces)} spaces)"
        )
    else:
        print("NetFloorArea: not available")

    if gross_count:
        print(
            f"GrossFloorArea: {gross_total:.2f} m² "
            f"({gross_count}/{len(spaces)} spaces)"
        )
    else:
        print("GrossFloorArea: not available")

    print("\nCOMPARISON")

    if net_count == len(spaces):
        difference = net_total - REPORTED_AREA
        percentage = difference / REPORTED_AREA * 100

        print(f"Reported area: {REPORTED_AREA:.2f} m²")
        print(f"IFC NetFloorArea: {net_total:.2f} m²")
        print(f"Difference: {difference:+.2f} m²")
        print(f"Difference: {percentage:+.2f} %")

    else:
        print(
            "A complete NetFloorArea comparison cannot be made because "
            "not all IfcSpaces contain NetFloorArea."
        )

    print("\nCONCLUSION")

    if net_count != len(spaces):
        print(
            "The reported floor area cannot currently be verified from "
            "the IFC because the area information is incomplete."
        )
    else:
        print(
            "The IFC provides a complete NetFloorArea value, but the "
            "client report does not state whether its reported area is "
            "net or gross. The numerical values can therefore be compared, "
            "but they cannot yet be treated as the same area definition."
        )


if __name__ == "__main__":
    main()
