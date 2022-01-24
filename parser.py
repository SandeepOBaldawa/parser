#!/usr/bin/env python3
#
# hacky conversion from ddql to promql, we will make this better incrementally
#

from pyparsing import *

DDOGQL_INPUT_FILE = "./input_ddogql.txt"

def preProcess(str):
    return str.translate(str.maketrans({".": "_"}))


def postProcess(str):
    str = str.translate(str.maketrans({":": '="', "}": '"}', ",": '",'}))
    str += ")"
    return str

#
# We can build & combine rules here 
# depending on the type of query
#
def parseTransformQuery(input):
  query_type = whichQuery(input) 
  if query_type == "sum":
    print("sum")
    rule = buildSumBaseRule()

    # pre-step
    ddql_str = preProcess(input)

    # grammar application
    res = rule.parse_string(ddql_str)

    # post-step
    res = postProcess("".join(res))
    return res
  elif query_type == "avg":
    print("avg")
  else:
    print("query rule not found")

def whichQuery(input):
  return input.split(':')[0]

# All Rules/Grammar
# Build Sum rule
def buildSumBaseRule():
    op_name = Word(alphanums)
    colon = one_of(":").set_parse_action(replace_with("("))
    key_word = OneOrMore(Word(alphanums + ",-_.{}:"))
    rule = op_name + colon + key_word
    return rule


def parseInputFile():
    print("===")
    try:
      with open(DDOGQL_INPUT_FILE, "r") as input_file:
        Lines = input_file.readlines()
        for idx, line in enumerate(Lines):
          res = parseTransformQuery(line)
          print("Input req: {0} ".format(idx),\
                "Ddql   ===> {0}".format(line.strip()),\
                "Promql ===> {0}".format(res), "===", sep='\n')
    except FileNotFoundError:
      msg = "Sorry, the file "+ DDOGQL_INPUT_FILE + "does not exist."
      print(msg)

def main():
  parseInputFile()

if __name__ == "__main__":
  main()
