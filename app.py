from bs4 import BeautifulSoup
import re
import os
import requests
import json


def load_page_content(page):
    url = 'http://localhost:5000/?page=%d' % page
    request = requests.get(url)
    return request.text


def page_contains_posts(text):
    soup = BeautifulSoup(text, 'lxml')
    post_list = soup.find('article', {'class': 'post'})
    return post_list is not None


def read_file(filename):
    with open(filename, mode='r', encoding='UTF-8') as input_file:
        text = input_file.read()
    return text


def parse_post_info(filename):
    results = []
    text = read_file(filename)

    soup = BeautifulSoup(text, 'lxml')
    posts_container = soup.find('div', {'class': 'main'})
    posts = posts_container.find_all('article', {'class': 'post'})
    for post in posts:
        post_link = post.find('header', {'class': 'post_head'}).find('a').get('href')
        post_link_text = post.find('header', {'class': 'post_head'}).find('a').text
        post_id = re.findall(r'\d+', post_link_text)
        post_body = post.find('div', {'class': 'post_body'}).text
        post_rating = post.find('div', {'class': 'post_total'}).text
        post_datetime = re.findall(r'\d{4}.\d{1,2}.\d{1,2}|\d\d:\d\d', post.find('div', {'class': 'post_footer_date'}).text)
        # time_post = post_datetime[1]
        date_post = re.sub(r'\.', '-', post_datetime[0])
        # date_post, time_post = re.match(r'(\d{4}.\d{1,2}.\d{1,2}) в(\d\d:\d\d)', post_datetime).groups()

        results.append({
            'post_id': post_id,
            'post_link': post_link,
            'post_body': post_body,
            'date_created': date_post,
            # 'time_create': time_post,
            'post_rating': post_rating
        })
    return results


def main():
    page = 1
    while True:
        data = load_page_content(page)
        if page_contains_posts(data):
            filename = 'C:\\Users\\Marcie\\Desktop\\pars_result\\page_%d.html' % page
            with open(filename, mode='w', encoding='UTF-8') as output_file:
                output_file.write(data)
                page += 1
        else:
            break

    results = []
    for filename in os.listdir('C:\\Users\\Marcie\\Desktop\\pars_result\\'):
        results.extend(parse_post_info('C:\\Users\\Marcie\\Desktop\\pars_result\\' + filename))
    resfile = 'posts.json'
    wfile = open(resfile, mode='w', encoding='UTF-8')
    json.dump(results, wfile, indent=4, ensure_ascii=False)
    wfile.close()


if __name__ == '__main__':
    main()
