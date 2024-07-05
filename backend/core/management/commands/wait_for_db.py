import time

from psycopg2 import OperationalError as Psycopg2Error

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
  """Retries connecting to PSQL until it's up"""
  def handle(self, *args, **kwargs):
    self.stdout.write('Waiting for db...')
    db_up = False
    while db_up is False:
      try:
        self.check(databases=['default'])
        db_up = True
      except (Psycopg2Error, OperationalError):
        self.stdout.write('Retrying connection in 1 second...')
        time.sleep(1)
    self.stdout.write(self.style.SUCCESS('Database up'))
