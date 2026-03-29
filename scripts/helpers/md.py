import os
import re
import math
import json
from scripts.helpers.utils import sort_api_list

def format_api_row(actor):
  api_name = actor.get('name') or ''
  api_url = actor.get('url') or '#'
  api_desc = actor.get('description') or ''
  api_rating = math.trunc(actor.get('rating', 0) * 100) / 100
  api_rating_count = actor.get('rating_count')

  name = re.sub(r'[|<>]', '', re.sub(r'\s+', ' ', api_name)).strip()
  description = re.sub(r'[|<>]', '', re.sub(r'\s+', ' ', api_desc)).strip()
  rating = f'⭐️ {api_rating} ({api_rating_count})' if api_rating > 0 else ''

  return f'| [{name}]({api_url}) | {rating} | {description} |'

def build_api_category_md(category: str, all_actors: list):
  slug = category.lower().replace('_', '-').replace(' ', '-')
  dir = f'{slug}-agent-apis'
  file_path = f'{dir}/README.md'
  
  os.makedirs(dir, exist_ok=True)
  with open(file_path, 'w', encoding='utf-8') as f:
    category_name = slug.title().replace('-', ' ')
    
    f.write('<a id="top"></a>\n')
    f.write(f'# 🤖 {category_name}\n\n')
    f.write(f'**Organized APIs by {category_name}**\n\n')
    f.write(f'**{len(all_actors)} APIs in this category**\n\n')

    f.write('| API | Rating | Description |\n')
    f.write('|-----|--------|-------------|\n')

    all_actors = sort_api_list(all_actors)

    for actor in all_actors:
      f.write(format_api_row(actor) + '\n')

    f.write('\n---\n\n')
    f.write('<p align="center">\n')
    f.write('  ⭐ Star this repo if you find it useful!<br/>\n')
    f.write('  🔝 <a href="#top">Back to top</a> • ')
    f.write('<a href="../README.md">⬅️ Back to Main</a>\n')
    f.write('</p>\n')

    f.write('\n<!--\n')
    f.write(f'keywords: {category_name}, AI agent APIs, automation APIs, LLM tools, agent tools, API directory\n')
    f.write('-->\n')

def build_main_readme(
  category_stats,
  readme_path='README.md'
):
  category_list = ''
  for c in sorted(category_stats, key=lambda x: x['name']):
    category_list += f"- 🤖 [{c['name']}]({c['slug']}) — **{c['count']:,} APIs**\n"

  category_sections = "## 🔥 Explore Agent APIs by Category\n\n"
  for c in sorted(category_stats, key=lambda x: x['count'], reverse=True):
    category_sections += f"### 🤖 {c['name']}\n"
    category_sections += f"📦 **{c['count']:,} APIs in this category** • [View all →]({c['slug']})\n\n"
    
    json_path = f"data/{c['slug']}.json"

    if os.path.exists(json_path):
      with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

      top_apis = data[:10]

      category_sections += '| API | Rating | Description |\n'
      category_sections += '|-----|--------|-------------|\n'

      for api in top_apis:
        category_sections += format_api_row(api) + '\n'

      category_sections += '\n---\n\n'

  total_apis = sum(c['count'] for c in category_stats)
  total_categories = len(category_stats)

  with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()

  content = re.sub(
    r'## 📚 API Categories\n\n.*?(?=\n## |\Z)',
    f'## 📚 API Categories\n\n{category_list.strip()}\n\n',
    content,
    flags=re.S
  )

  content = re.sub(
    r'## 🔥 Explore APIs by Category\n\n.*?(?=\n## |\Z)',
    '',
    content,
    flags=re.S
  )

  content = content.replace(
    '## 📚 API Categories',
    f'## 📚 API Categories\n\n{category_list.strip()}\n\n---\n\n{category_sections.strip()}'
  )

  content = re.sub(r'APIs-\d+', f'APIs-{total_apis}', content)
  content = re.sub(r'Categories-\d+', f'Categories-{total_categories}', content)

  with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)
