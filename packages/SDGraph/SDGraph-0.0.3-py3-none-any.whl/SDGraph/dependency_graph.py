#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys

from networkx.drawing.nx_agraph import to_agraph

from .dependency_analysis import FileStaticAnalysis

SUPPORTED_FORMAT = ['dot', 'org', 'all', 'txt']


class DependencyGraph():
  GIT_ROOT = None

  def __init__(self, starts):
    if DependencyGraph.GIT_ROOT is None:
      DependencyGraph.GIT_ROOT = FileStaticAnalysis.get_git_root(starts[0])

    def get_relpath(path):
      return os.path.relpath(path, DependencyGraph.GIT_ROOT)

    self.files = set(map(get_relpath, starts))
    self.G = None
    self.explored = set()

  def get_graph(self):
    if self.G:
      return self.G

    while len(self.files) > 0:
      file_relpath = self.files.pop()

      print("[INFO] start explore :", file_relpath)
      self.explored.add(file_relpath)

      file_realpath = os.path.join(DependencyGraph.GIT_ROOT, file_relpath)
      file_analyzer = FileStaticAnalysis(file_realpath, G=self.G)
      self.G = file_analyzer.get_graph()
      self.files |= (set(self.G.node) - self.explored)

      print("[INFO] complete explore: ", file_relpath)
      print("[INFO] remaining files: ", len(self.files))

    return self.G

  def get_dependency_list(self):
    G = self.get_graph()
    return G.nodes()

  def save_dot(self, filename):
    G = self.get_graph()
    agraph = to_agraph(G)
    agraph.layout('dot')
    agraph.write(filename + ".dot")
    agraph.draw(filename + ".png")

  def save_org(self, filename):
    G = self.get_graph()
    edges = sorted(G.edges(data=True))

    header_file_path = os.path.join(
      os.path.dirname(__file__),
      "org_header.org"
    )

    with open(header_file_path, "r") as f:
      context = f.readlines()

    current_file = ""
    while len(edges) > 0:
      src, dest, data = edges.pop()
      if current_file != src:
        current_file = src
        context.append("* " + src + "\n")

      context.append("** " + dest + "\n")
      for var, varType in data.items():
        context.append("- {name} :: {type} \n".format(name=var, type=varType))

    with open(filename + ".org", "w") as f:
      f.writelines(context)

  def save_list(self, filename):
    dep_list = self.get_dependency_list()
    with open('{0}.txt'.format(filename), 'w') as f:
      f.writelines([l + '\n' for l in dep_list])

  def make_report(self, name):
    self.save_dot(name)
    self.save_org(name)
    self.save_list(name)


def check_args(args):
  if len(args.filenames) <= 0:
    print('You need to give at one python file to analysis')
    sys.exit(1)

  if not all(format in SUPPORTED_FORMAT for format in args.output_format):
    print('All {0} should in list: {1}'.format(args.output_format,
                                               SUPPORTED_FORMAT))
    sys.exit(1)


def parse_args():
  parser = argparse.ArgumentParser(description='Python Dependency Graph Generator')
  parser.add_argument(
    '-f',
    '--filenames',
    nargs='+',
    type=str,
    help='python files that we want to analysis')
  parser.add_argument(
    '-o',
    '--output-format',
    nargs='+',
    type=str,
    help='output format for the dependency list: {0}'.format(SUPPORTED_FORMAT))
  parser.add_argument(
    '-n',
    '--output-name',
    type=str,
    default='dep_list',
    help='output file name for the dependency list')

  args = parser.parse_args()
  check_args(args)
  return args


def main():
  args = parse_args()
  graph_analyzer = DependencyGraph(args.filenames)

  if 'all' in args.output_format:
    graph_analyzer.make_report(args.output_name)
    return

  if 'dot' in args.output_format:
    graph_analyzer.save_dot(args.output_name)
  if 'org' in args.output_format:
    graph_analyzer.save_org(args.output_name)
  if 'txt' in args.output_format:
    graph_analyzer.save_list(args.output_name)


if __name__ == '__main__':
    main()
