#!/usr/bin/python3
import operator
from pathlib import Path
from slugify import slugify

def get_yaml_files(path):
    exts = ('*.yaml', "*.yml")
    yaml_dir = Path(path)
    yaml_files = [f for f in yaml_dir.iterdir() if any(f.match(p) for p in exts) ]
    return yaml_files

def validate_obj(obj: dict, key_set: list):
    for key in key_set:
        if key not in obj.keys():
            raise KeyError(f"❌ Missing required key: {key} in {next(iter(obj.values()))}")

        if 'slug' in obj.keys():
            slug_validation = slugify(obj.get('slug'))
            if obj.get('slug') != slug_validation:
                raise KeyError(f"❌ {obj.get('slug')} does not meet standard; must be changed to {slug_validation}")

def get_nb_objs(nb, api_attr):
    return operator.attrgetter(api_attr)(nb).all()

def create_obj(nb, output_name, api_attr, nb_obj) -> None:
    try:
        result = operator.attrgetter(api_attr)(nb).create(nb_obj)
        print(
            f"✅ {output_name}: '{str(result).replace('[', '').replace(']', '')}' successfully created")
    except RequestError as e:
        err_msg = ast.literal_eval(e.error)
        for err in err_msg:
            if len(err) != 0:
                print(
                    f"❌ {output_name} '{list(err.keys())[0]}' - {', '.join(list(err.values())[0])}")
