import os
import json
from scripts.scrapers.Apify import ApifyScraper
from scripts.helpers.utils import sort_api_list
from scripts.helpers.md import build_api_category_md, build_main_readme

os.makedirs('data', exist_ok=True)

def merge_data(old, new):
  data_map = {item['id']: item for item in old}

  for item in new:
    key = item['id']

    if key in data_map:
      data_map[key]['rating'] = item.get('rating', data_map[key].get('rating'))
      data_map[key]['rating_count'] = item.get('rating_count', data_map[key].get('rating_count'))
      data_map[key]['description'] = item.get('description', data_map[key].get('description'))
    else:
      data_map[key] = item

  return list(data_map.values())

def main():
  apify = ApifyScraper()
  categories = apify.get_category_list()

  category_stats = []

  for category in categories:
    count = 1000
    offset = 0
    all_actors = []

    while True:
      print(f'Category {category} - {offset}')
      
      actors = apify.get_popular_actors(
        count=count,
        offset=offset,
        category=category
      )

      if not actors:
        break

      all_actors.extend(actors)
      offset += count

    slug = category.lower().replace('_', '-').replace(' ', '-')
    dir_name = f'{slug}-agent-apis'
    json_path = f'data/{slug}-agent-apis.json'

    all_actors = list({
      actor.get('id'): actor
      for actor in all_actors if actor.get('id')
    }.values())

    if os.path.exists(json_path):
      with open(json_path, 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    else:
      old_data = []

    merged_data = merge_data(old_data, all_actors)
    merged_data = sort_api_list(merged_data)

    with open(json_path, 'w', encoding='utf-8') as f:
      json.dump(merged_data, f, ensure_ascii=False, indent=2)

    build_api_category_md(category, merged_data)
    print(f'Updated {category}: {len(merged_data)} APIs')

    category_name = slug.title().replace('-', ' ')
    category_stats.append({
      'name': category_name,
      'count': len(merged_data),
      'slug': dir_name
    })

  build_main_readme(category_stats)
  print('🤙🏻')

if __name__ == '__main__':
  main()
  