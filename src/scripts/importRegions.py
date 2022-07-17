#!/usr/bin/python3
import yaml
import pynetbox
from pprint import PrettyPrinter, pformat
import os
import emoji
from dotenv import load_dotenv
from netbox import create_obj, validate_obj, get_yaml_files, get_nb_objs
import logging
import logging.config


alert = "\U0001F6A8"
hour_glass = "\U000023F3"
globe = "\U0001F30D"
OK = "\U0001F197"

def create_child_regions(obj: dict, nb: pynetbox.api, existing_regions: list):
    nb_regions = existing_regions
    if obj.get('children'):
        required_keys = ['name', 'slug', 'parent']
        parent_id = nb.dcim.regions.get(slug=obj.get('slug')).id
        child_objects = obj.get('children')
        for child in child_objects:
            child['parent'] = parent_id
            validate_obj(child, required_keys)
            if child.get('slug') not in nb_regions:
                create_obj(nb, 'regions', 'dcim.regions', child)
            else:
                print(f"{globe} {child.get('name')} region exists")
            if child.get('children'):
                create_child_regions(child, nb, nb_regions)

def create_regions(region_files: list, nb: pynetbox.api, existing_regions: classmethod, required_keys: list):
    nb_regions = [ x.slug for x in existing_regions ]
    required_keys = required_keys
    for file in region_files:
        with open(file, 'r') as f:
            stream = yaml.safe_load(f)
            regions = stream.get('regions')
            for region in regions:
                validate_obj(region, required_keys)
                if region.get('slug') not in nb_regions:
                    create_obj(nb, 'regions', 'dcim.regions', region)
                else:
                    print(f"{globe} {region.get('name')} region exists")
                if region.get('children'):
                    create_child_regions(region, nb, nb_regions)

def create_nb_regions(nb, REGIONS_DIR):
    print(f"{hour_glass} Retrieving existing Netbox Regions")
    existing_regions = get_nb_objs(nb,"dcim.regions")
    required_keys = ['name', 'slug']
    REGION_FILES = get_yaml_files(REGIONS_DIR)
    create_regions(REGION_FILES, nb, existing_regions, required_keys)
