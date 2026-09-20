# Hej med dig 
# :3
#ser om bæstet virker...
from pathlib import Path

try:
    import ifcopenshell
except ModuleNotFoundError as error:
    if error.name != "ifcopenshell":
        raise
    raise SystemExit(
        "ERROR: IfcOpenShell is not installed in this Python environment. "
        "Install it using: python -m pip install ifcopenshell"
    ) from error

modelname = "B308X.ifc"

dir_path = Path(__file__).resolve().parent
model_url = dir_path / "model" / modelname

if not model_url.is_file():
    raise SystemExit(f"ERROR: IFC model not found: {model_url}")

try:
    model = ifcopenshell.open(str(model_url))
except (OSError, RuntimeError) as error:
    raise SystemExit(f"ERROR: Could not open {model_url}: {error}") from error

# Your script goes here

# Test if everything works:
spaces_required = 21
spaces_in_model = len(model.by_type("IfcSpace"))

print(f"\nThere are {spaces_in_model} spaces in the model")

if spaces_required == spaces_in_model:
    print ('RESULT: The number of spaces is correct')
else:
    print(f"RESULT: Expected {spaces_required} spaces, found {spaces_in_model}")
