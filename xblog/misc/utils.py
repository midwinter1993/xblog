#!/usr/bin/env python
# -*- coding: utf-8 -*-


import codecs
import os
import shutil
import json
import jinja2
import subprocess
import datetime
import time
import distutils


class XExecption(Exception):
    pass


def save_file(fpath, fcontent):
    with codecs.open(fpath, 'w', 'utf-8') as fp:
        fp.write(fcontent)


def load_file(fpath):
    with codecs.open(fpath, 'r', 'utf-8') as fp:
        return fp.read()


def load_json(fpath):
    if not os.path.exists(fpath):
        raise XExecption('Json file `%s` does not exist.' % fpath)
    return json.loads(load_file(fpath))


def load_template(template_fpath):
    loader = jinja2.FileSystemLoader(parent_dir(template_fpath))
    environment = jinja2.Environment(loader=loader)
    return environment.get_template(os.path.basename(template_fpath))
    #  return jinja2.Template(load_file(template_fpath))


def base_name(fpath):
    return os.path.splitext(os.path.basename(fpath))[0]


def run_command(cmd, is_prompt=True):
    if is_prompt:
        print('[ RUN ]', ' '.join(cmd))
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    return stdout, stderr


def git_branch():
    stdout, stderr = run_command(['git', 'branch'])
    branches = stdout.decode('utf-8').split('\n')
    for b in branches:
        if '*' in b:
            return b[2:]
    return 'None'


#  def copy_to(dst, src):
    #  if os.path.exists(dst):
        #  shutil.rmtree(dst)
    #  shutil.copytree(src, dst)

def find_package_dir():
    lib_dir = distutils.sysconfig.get_python_lib()

    for d in os.listdir(lib_dir):
        if d == 'xblog':
            if os.path.isdir(os.path.join(lib_dir, d)):
                return os.path.join(lib_dir, d)
            else:
                raise XExecption('xblog is not a package')

    raise XExecption('This package not found under `%s`' % lib_dir)


def list_dir(d):
    if not os.path.exists(d):
        print(d, 'not exists.')
        return
    #  for f in os.listdir(d):
        #  yield os.path.join(d, f)

    for path, dirs, files in os.walk(d):
        for f in files:
            yield os.path.join(path, f)


def parent_dir(path):
    return os.path.abspath(os.path.join(path, os.pardir))


def mk_dir(dpath, is_prompt=True):
    if is_prompt:
        if os.path.exists(dpath):
            print('[ MK DIR ]', dpath, '*EXISTS*')
        else:
            print('[ MK DIR ]', dpath)
    run_command(['mkdir', '-p', dpath], False)


def _remove(path):
    if os.path.exists(path):
        run_command(['rm', '-rf', path], False)
    else:
        print(path, 'does not exist.')


def rm_dir(dpath, is_prompt=True):
    if is_prompt:
        print('[ RM DIR ]', dpath)
    _remove(dpath)


def rm_file(fpath, is_prompt=True):
    if is_prompt:
        print('[ RM FILE ]', fpath)
    _remove(fpath)


def clean_dir(dpath):
    print('[ CLEAN DIR ]', dpath)
    if os.path.exists(dpath):
        rm_dir(dpath, False)
        mk_dir(dpath, False)
    else:
        print(dpath, 'does not exist.')


def is_empty_dir(dpath):
    files = [f for f in os.listdir(dpath)]
    return len(files) == 0


def _prepare_paths(from_path, to_path, is_overwrite):
    if not os.path.exists(from_path):
        raise XExecption(from_path + ' does not exists.')

    if os.path.exists(to_path):
        if is_overwrite:
            rm_dir(to_path, False)
            print('[ OVERWRITE ]', to_path)
        else:
            raise XExecption(to_path + ' exists.')


def _move(from_path, to_path, is_overwrite=False):
    _prepare_paths(from_path, to_path, is_overwrite)
    run_command(['mv', from_path, to_path], False)


def _copy(from_path, to_path, is_overwrite=False):
    _prepare_paths(from_path, to_path, is_overwrite)
    run_command(['cp', '-r', from_path, to_path], False)


def move_dir(from_path, to_path):
    _move(from_path, to_path, is_overwrite=True)
    print('[ MOVE DIR ] from `%s` to `%s`' % (from_path, to_path))


def move_file(from_path, to_path):
    _move(from_path, to_path, is_overwrite=True)
    print('[ MOVE FILE ] from `%s` to `%s`' % (from_path, to_path))


def copy_dir(from_path, to_path):
    _copy(from_path, to_path, is_overwrite=True)
    print('[ COPY DIR ] from `%s` to `%s`' % (from_path, to_path))


def copy_file(from_path, to_path):
    _copy(from_path, to_path, is_overwrite=True)
    print('[ COPY FILE ] from `%s` to `%s`' % (from_path, to_path))


def file_mod_tsc(fpath):
    if not os.path.exists(fpath):
        raise XExecption(fpath + ' does not exists.')
    return os.path.getmtime(fpath)
