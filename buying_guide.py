import os

from requests import post
from dotenv import load_dotenv
load_dotenv()
import openai
import base64

openai.api_key = os.getenv('openai_api')

wp_user = os.getenv('user')
wp_pass = os.getenv('pass')
wp_credential = f'{wp_user}:{wp_pass}'
wp_token = base64.b64encode(wp_credential.encode('utf-8'))
wp_headers = {'Authorization':'Basic '+wp_token.decode()}

file = open('keyword.text')
keywords = file.readlines()
file.close()

def openai_answer(prompt):
  response = openai.Completion.create(
    model="text-davinci-002",
    prompt=prompt,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  ai_data = response.get('choices')[0].get('text').strip('\n')
  return ai_data

def wp_heading_two(text):
  heading = f'<!-- wp:heading --><h2>{text}</h2><!-- /wp:heading -->'
  return heading

def wp_paragraph(text):
  pragraph = f'<!-- wp:paragraph --><p>{text}</p><!-- /wp:paragraph -->'
  return pragraph


def slugify(text):
  code = text.strip().replace(' ', '-')
  return code



for keyword in keywords:
  keyword = keyword.strip('\n')


  intro_prompt = f'write a short description about {keyword}'
  important_prompt = f'write why {keyword} is important'
  how_prompt = f"write a paragraph about 'how to choose best' {keyword}"
  consider_prompt = f"write a 200 word about '5 things to Consider while buying' {keyword}"
  conclusion_prompt = f'Write a 100 word blog conclusion on {intro_prompt}'

  slug = slugify(keyword)
  wp_title = f'Write a Buying Guide About The Best {keyword.title()}'

  h2_important = f'Why {keyword.title()} Is Important'
  h2_how = f'How to Choose The Best {keyword.title()}'
  h2_consider = f'Things to Consider While Buying {keyword.title()}'



  header_intro = wp_paragraph(openai_answer(intro_prompt))
  pra_one = wp_heading_two(h2_important) + wp_paragraph(openai_answer(important_prompt))
  pra_two = wp_heading_two(h2_how) + wp_paragraph(openai_answer(how_prompt))
  pra_three = wp_heading_two(h2_consider) + wp_paragraph(openai_answer(consider_prompt))
  conclusion = wp_heading_two('Conclusion') + wp_paragraph(openai_answer(conclusion_prompt))
  content = f'{header_intro}{pra_one}{pra_two}{pra_three}{conclusion}'



  def wp_posting(wp_title, slug, content):
    api_url = 'https://localhost/mobile-phone/wp-json/wp/v2/posts'
    data = {
      'title': wp_title,
      'slug': slug,
      'content': content
    }
    res = post(url=api_url, data=data, headers=wp_headers, verify=False)
    print(res)
  wp_posting(wp_title, slug, content)

