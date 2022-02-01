#!/usr/bin/python3
import os

FILENAME='netbox_dump.sql.gz'
def backup():

    os.system("docker-compose exec postgres sh -c 'pg_dump -cU $POSTGRES_USER $POSTGRES_DB' | gzip > {}".format(FILENAME))

def restore():
    os.system("docker-compose stop netbox netbox-worker netbox-housekeeping")
    os.system("gunzip -c db_dump.sql.gz | docker-compose exec -T postgres sh -c 'psql -U $POSTGRES_USER $POSTGRES_DB'")
    os.system("docker-compose start netbox netbox-worker netbox-housekeeping")


