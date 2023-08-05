#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

import git
import jedi
import networkx as nx


class FileStaticAnalysis():
  """ Static python script dependency analyzer """
  GIT_ROOT = None

  @staticmethod
  def get_git_root(path):
    try:
      git_repo = git.Repo(path, search_parent_directories=True)
      git_root = git_repo.git.rev_parse("--show-toplevel")
    except Exception as e:
      print("fail to find git root path automatically, error: {}".format(e))
      print("hardcode git root path using PY3_DEP_ROOT")
      git_root = os.getenv('PY3_DEP_ROOT')
    return git_root

  def __init__(self, file_path, G=None, sys_path=None):
    if FileStaticAnalysis.GIT_ROOT is None:
      FileStaticAnalysis.GIT_ROOT = FileStaticAnalysis.get_git_root(file_path)

    self.sys_path = sys_path or sys.path
    self.file_path = file_path
    self.file_relpath = os.path.relpath(file_path, FileStaticAnalysis.GIT_ROOT)
    self.var_names = FileStaticAnalysis._extract_var_names(file_path)
    self.G = G or nx.DiGraph()

  @staticmethod
  def _extract_var_names(filename):
    if not filename.endswith(".py"):
      return []

    try:
      var_names = jedi.names(path=filename)
      return var_names
    except:
      return []

  def _is_define_in_same_file(self, var):
    if var.module_path is not None:
      return os.path.samefile(var.module_path, self.file_path)
    return False

  def _is_under_same_git_root(self, var):
    if var.module_path is not None:
      return FileStaticAnalysis.GIT_ROOT in var.module_path
    return False

  def var_def_iter(self):
    def p_l_pair(var_name):
      return {"line": var_name.line,
              "column": var_name.column}

    def make_script(p_l_pair):
      return jedi.Script(path=self.file_path,
                         sys_path=self.sys_path,
                         **p_l_pair)

    p_l_pairs = (p_l_pair(var_name) for var_name in self.var_names)
    scripts = (make_script(p_l_pair) for p_l_pair in p_l_pairs)

    for script in scripts:
      try:
        var_defs = script.goto_definitions()
        for var in var_defs:
          if not any([var.in_builtin_module(),
                      self._is_define_in_same_file(var),
                      not self._is_under_same_git_root(var)]):
            yield {
              "type": var.type,
              "name": var.name,
              "path": var.module_path
            }
      except:
        print("[WARNING] ", self.file_path, script._pos)
    raise StopIteration

  def get_graph(self):
    for bag in self.var_def_iter():
      if bag["path"] is not None:
        u = self.file_relpath
        v = os.path.relpath(bag["path"], start=FileStaticAnalysis.GIT_ROOT)
        self.G.add_edge(u, v)
        self.G.get_edge_data(u, v)[bag["name"]] = bag["type"]
    return self.G
