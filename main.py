# from scraper import getTvShowData 
import argparse
from scraper import getTvShowData

parser = argparse.ArgumentParser(
  prog='IMDB Scraper',
  description='A simple scraper for IMDB',
  allow_abbrev=False
)

parser.add_argument(
  'id',
  type=str,
  help='TV show ID'
)

args = parser.parse_args()
getTvShowData(args.id)