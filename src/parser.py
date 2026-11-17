import requests
import bs4
import sqlite3


class ForumParser():
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    def fetch(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.text

    def parse_html(self, html):
        bs = bs4.BeautifulSoup(html, 'lxml')
        parsed_data = []
        
        #все таблицы с классом ipbtable и атрибутом data-post
        for post in bs.find_all('table', class_='ipbtable'):
            if not post.has_attr('data-post'):
                continue
            try:
                comment_id = int(post['data-post'])
                
                name_tag = post.find('span', class_='normalname')
                name = name_tag.get_text(strip=True) if name_tag else "Unknown" #обрезает невидимые символы в начале и в конце строки
                
                message_tag = post.find('div', class_='postcolor')
                message = message_tag.get_text(separator=' ', strip=True) if message_tag else "No text"  

                parsed_data.append({
                    'id': comment_id,
                    'name': name,
                    'message': message
                })
            except Exception:
                continue
                
        return parsed_data

    def parse_page(self, url):
        html = self.fetch(url)
        return self.parse_html(html)

    def save_to_db(self, parsed_data, repository):
        count = 0
        for item in parsed_data:
            try:
                repository.add(item['id'], item['name'], item['message'])
                count += 1
            except sqlite3.IntegrityError:
                continue
        return count