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
            raise utils.XExecption('Invalid post name [%s].' % post_path)

        self._render()

    def title(self):
        return self.name_.replace('-', ' ')

    def is_private(self):
        return self.meta().get('type', 'private') == 'private'

    def is_public(self):
        return not self.is_private()

    def relative_path(self):
        if self.is_private():
            return os.path.join('site', 'posts', 'private', self.htmlname())
        else:
            return os.path.join('site', 'posts', 'public', self.htmlname())

    def filename(self):
        return self.name_

    def htmlname(self):
        return self.filename() + '.html'

    def meta(self):
        return self.meta_

    def content(self):
        return self.rendered_md_

    def html(self):
        return self.html_content_

    def date(self):
        # post name: yy_mm_dd_name1-name2-name3
        base_path = utils.base_name(self.path_)
        date = list(map(int, base_path.split('_')[:3]))
        return datetime.datetime(date[0], date[1], date[2])

    def _render(self):

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
        posts.sort(key=lambda i: i.date(), reverse=True)
        return posts

    @staticmethod
    def generatePosts(config):
        post_dir = config['post_dir']
        site_dir = config['site_dir']

        posts = Post.collectPosts(post_dir)
        if config['args']['--public']:
            posts = list(filter(lambda p: p.is_public(), posts))

        for post in posts:
            html_fpath = post.relative_path()
            utils.save_file(html_fpath, post.html())
            print('[POST GEN]', post.title(), '==>', post.relative_path())

        print('Total:', len(posts), 'posts')
        return posts
