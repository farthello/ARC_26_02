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
spaces_required = 21
spaces_in_model = 0

for entity in model.by_type("IfcSpace"):
    spaces_in_model+=1

print(f"\nThere are {spaces_in_model} spaces in the model")

if spaces_required is spaces_in_model:
    print ('RESULT: The number of spaces is correct')
else:
    print ('RESULT: The number of spaces is wrong')