import json
import os
import argparse

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def render_website(json_path):
    os.makedirs('pages', exist_ok=True)

    with open(json_path, 'r') as all_books:
        books = json.load(all_books)


    books_per_page = 10
    pages = list(chunked(books, books_per_page))

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    env.filters['chunked'] = chunked
    template = env.get_template('template.html')

    for page_num, page in enumerate(pages, start=1):
        rendered_page = template.render(books=page, current_page=page_num, total_pages=len(pages))

        page_filename = f'pages/index{page_num}.html'
        with open(page_filename, 'w', encoding='utf8') as file:
            file.write(rendered_page)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--json-path',
        default='media/all_books.json',
        help='Path to the data file'
    )
    args = parser.parse_args()

    render_website(args.json_path)

    server = Server()
    server.watch('template.html', render_website)
    server.serve(root='.', default_filename='pages/index1.html')
