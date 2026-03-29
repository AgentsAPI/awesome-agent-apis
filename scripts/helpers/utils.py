def api_score(item, m, C):
  R = item.get('rating', 0)
  v = item.get('rating_count', 0)
  return (v / (v + m)) * R + (m / (v + m)) * C if (v + m) else 0

def sort_api_list(apis):
  m = 50
  C = sum(x['rating'] for x in apis) / len(apis)
  apis.sort(key=lambda x: api_score(x, m, C), reverse=True)

  return apis
  
