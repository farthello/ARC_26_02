from pathlib import Path
import ifcopenshell
import ifcopenshell.util.element as util_element
import ifcopenshell.util.unit as util_unit

modelname = "B308X.ifc"

try:
    dir_path = Path(__file__).parent
    model_url = Path.joinpath(dir_path, 'model', modelname).with_suffix('.ifc')
    model = ifcopenshell.open(model_url)
except OSError:
    try:
        import bpy
        model_url = Path.joinpath(Path(bpy.context.space_data.text.filepath).parent, 'model', modelname).with_suffix('.ifc')
        model = ifcopenshell.open(model_url)
    except OSError:
        print(f"ERROR: please check your model folder : {model_url} does not exist")

# Your script goes here

def get_gross_floor_area(space):
    """
    Look specifically for GrossFloorArea in any Qto_* quantity set.
    Returns (area, source) or (None, reason) if not found/zero.
    """
    psets = util_element.get_psets(space, qtos_only=True)

    for qset_name, qset in psets.items():
        if "GrossFloorArea" in qset and qset["GrossFloorArea"]:
            return qset["GrossFloorArea"], qset_name

    return None, "No non-zero GrossFloorArea found in any quantity set"


# Use the AREA unit scale directly - do NOT square the length unit scale,
# since IFC allows area units to be defined independently of length units.
area_unit_scale = util_unit.calculate_unit_scale(model, unit_type="AREAUNIT")

total_area = 0.0
print("\nSpace gross floor areas:")
for space in model.by_type("IfcSpace"):
    name = space.Name or space.LongName or space.GlobalId

    area, source = get_gross_floor_area(space)
    if area is not None:
        area_m2 = area * area_unit_scale
        total_area += area_m2
        print(f"  {name}: {area_m2:.2f} m²  (source: {source})")
    else:
        print(f"  {name}: could not determine gross floor area ({source})")

print(f"\nTotal gross floor area across {len(model.by_type('IfcSpace'))} spaces: {total_area:.2f} m²")