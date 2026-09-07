# Hej med dig 
# :3
#ser om bæstet virker...
from pathlib import Path
import ifcopenshell

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

# Test if everything works:
spaces = model.by_type("IfcSpace")
for space in spaces:
    print(space.LongName)