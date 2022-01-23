#!/usr/bin/env python3
#
# hacky conversion from ddql to promql, we will make this better incrementally
#
from pyparsing import *

# Run before parsing
def preProcess(str):  
  return str.translate(str.maketrans({".": "_"}))

# Run after parsing 
def postProcess(str):  
  str = str.translate(str.maketrans({":": '="', "}": '"}', ",":'",'}))
  str += ")"
  return str

# Rules/Grammar 
op_name = Word(alphanums)
colon = one_of(":").set_parse_action(replace_with("("))
key_word = OneOrMore(Word(alphanums + ",-_.{}:"))
rule = op_name + colon + key_word

expected_promql_str1 = 'sum(kubernetes_state_container_ready{container="carts"})'
expected_promql_str2 = 'sum(kubernetes_state_container_restarts{container="carts"})'

print("===")
def parseInputFile():
  file = open('input_ddogql.txt', 'r')
  Lines = file.readlines()
  for idx,line in enumerate(Lines):
    ddql_str = preProcess(line)
    res = rule.parse_string(ddql_str)
    res = postProcess("".join(res))
    print("Input req:", idx) 
    print("Ddql   ===>", line.strip())
    print("Promql ===>", res)
    print("===")

parseInputFile()
