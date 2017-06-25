#!/usr/env python3
import re
import glob


def get_all_pages():
    pages = []
    for file in glob.glob("html/*.html"):
        pages.append(get_page(file[5:-5]))
    return pages


def get_page(page):
    template(page)
    return template(page)


def css(stylesheet):
    with open('html/' + stylesheet + '.css', 'r') as f:
        style = f.read()
        style = '<style type="text/css">' + style + '</style>'
        return style


def javascript(script):
    with open('html/' + script + '.js', 'r') as f:
        script = f.read()
        script = '<script>' + script + '</script>'
        return script


def template(name):
    name = 'html/' + name + '.html'
    with open(name, 'r') as f:
        page = f.read()
    for x in re.findall(r'\{\{templates/([^}]+)\}\}', page):
        page = re.sub(r'\{\{templates/([^}]+)\}\}',
                      template('templates/' + x),
                      page,
                      count=1)
    for x in re.findall(r'\{\{css/([^}]+)\}\}', page):
        page = re.sub(r'\{\{css/([^}]+)\}\}',
                      css('css/' + x),
                      page,
                      count=1)
    for x in re.findall(r'\{\{js/([^}]+)\}\}', page):
        page = re.sub(r'\{\{js/([^}]+)\}\}',
                      javascript('js/' + x),
                      page,
                      count=1)
    return page
