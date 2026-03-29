import requests

class ApifyScraper():
  def __init__(self):
    self.api_url = 'https://ow0o5i3qo7-2.algolianet.com/1/indexes/prod_PUBLIC_STORE_bookmarkCount_desc/query'
    self.headers = {
      'content-type': 'application/json',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
      'x-algolia-api-key': '0ecccd09f50396a4dbbe5dbfb17f4525',
      'x-algolia-application-id': 'OW0O5I3QO7'
    }

  def get_category_list(self):
    return [
      'AGENTS', 'AI', 'AUTOMATION',
      'DEVELOPER_TOOLS', 'ECOMMERCE', 'INTEGRATIONS',
      'JOBS', 'LEAD_GENERATION', 'MCP_SERVERS',
      'NEWS', 'OPEN_SOURCE', 'REAL_ESTATE', 'SEO_TOOLS',
      'SOCIAL_MEDIA', 'TRAVEL', 'VIDEOS', 'OTHER'
    ]
  
  def extract_apify_actor(self, actor):
    return {
      'id': actor.get('objectID'),
      'name': actor.get('title', ''),
      'description': actor.get('description', ''),
      'rating': actor.get('actorReviewRating'),
      'rating_count': actor.get('actorReviewCount'),
      'url': f'https://apify.com/{actor.get('username')}/{actor.get('name')}?fpr=hs6s8'
    }

  def get_popular_actors(
    self,
    count: int = 10,
    offset: int = 0,
    category: str = None
  ):
    payload = {
      'query': '',
      'length': count,
      'offset': offset,
      'restrictSearchableAttributes': [],
      'attributesToHighlight': [],
      'attributesToRetrieve': [
        'objectId',
        'title',
        'name',
        'username',
        'description',
        'actorReviewRating',
        'actorReviewCount'
      ],
      'enableABTest': True,
      'analyticsTags': ['web', 'store-search'],
      'clickAnalytics': True,
      'userToken': ''
    }
    if category:
      payload['filters'] = f'categories:{category}'

    try:
      res = requests.post(self.api_url, json=payload, headers=self.headers)
      res.raise_for_status()
      
      data = res.json()
      actors = data.get('hits', [])

      results = []
      for actor in actors:
        if actor:
          results.append(self.extract_apify_actor(actor))

      return results
    except Exception as err:
      print(err)
      return None

