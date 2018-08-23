#!/usr/bin/env python
# -*- coding: utf-8 -*-


import markdown2
import datetime
import os

from xblog.misc import utils


class Post(object):
    def __init__(self, post_path):
        super(Post, self).__init__()
        # post path: /path/to/yy_mm_dd_name1-name2-name3.md
        # or /path/to/yy_mm_dd.md
        self.path_ = post_path
        lst = utils.base_name(post_path).split('_')
        if len(lst) == 4:
            self.name_ = lst[-1]
        elif len(lst) == 3:
            self.name_ = '_'.join(lst)
        else:
            raise utils.XExecption('Invalid post name `%s`.' % post_path)

        if self.need_render():
            self._render()

    def title(self):
        return self.name_.replace('-', ' ')

    def md_path(self):
        return self.path_

    def html_path(self):
        return os.path.join('site', 'posts', self.htmlname())

    def filename(self):
        return self.name_

    def htmlname(self):
        return self.filename() + '.html'

    def meta(self):
        return self.meta_

    def content(self):
        # Interface for jinja2 template
        return self.rendered_md_

    def html(self):
        return self.html_content_

    def post_date(self):
        # post name: yy_mm_dd_name1-name2-name3
        base_path = utils.base_name(self.path_)
        date = list(map(int, base_path.split('_')[:3]))
        return datetime.datetime(date[0], date[1], date[2])

    def need_render(self):
        if not os.path.exists(self.html_path()):
            return True
        html_mod_tsc = utils.file_mod_tsc(self.html_path())
        md_mod_tsc = utils.file_mod_tsc(self.md_path())

        return html_mod_tsc < md_mod_tsc

    def _render(self):
        assert self.need_render()

        self.rendered_md_ = markdown2.markdown_path(path=self.path_,
                                                    extras=['fenced-code-blocks',
                                                            'metadata'])
        self.meta_ = self.rendered_md_.metadata

        config = utils.load_json('./config.json')
        post_template = utils.load_template(config['theme']['post'])
        self.html_content_ = post_template.render(config=config,
                                                  post=self)

    @staticmethod
    def collectPosts(post_dir):
        posts = [Post(f) for f in utils.list_dir(post_dir) if f.endswith('.md')]
        posts.sort(key=lambda i: i.post_date(), reverse=True)
        return posts

    @staticmethod
    def generatePosts(config):
        post_dir = config['post_dir']
        site_dir = config['site_dir']

        posts = Post.collectPosts(post_dir)

        for post in posts:
            html_fpath = post.html_path()
            if post.need_render():
                utils.save_file(html_fpath, post.html())
                print('[ GEN POST ]', post.title(), '==>', post.html_path())

        print('Total:', len(posts), 'posts')
        return posts
