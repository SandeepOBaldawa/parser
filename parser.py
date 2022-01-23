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

  return str.translate(str.maketrans({":": '="', "}": '"}'}))



# Rules/Grammar 

op_name = Word(alphanums)

colon = one_of(":").set_parse_action(replace_with("("))

key_word = OneOrMore(Word(alphanums + "_.{}:"))

rule = op_name + colon + key_word



ddql_str1 = "sum:kubernetes_state.container.ready{container:carts}"

print("Datadog Query 1 ==>", ddql_str1)

ddql_str2 = "sum:kubernetes_state.container.restarts{container:carts}"

print("Datadog Query 2 ==>", ddql_str2)

ddql_str1 = preProcess(ddql_str1)

ddql_str2 = preProcess(ddql_str2)



expected_promql_str1 = 'sum(kubernetes_state_container_ready{container="carts"})'

expected_promql_str2 = 'sum(kubernetes_state_container_restarts{container="carts"})'



print("====")

res1 = rule.parse_string(ddql_str1)

res1.append(")")

res1 = postProcess("".join(res1))

print("Promql Query 1 ==>", res1)



res2 = rule.parse_string(ddql_str2)

res2.append(")")

res2 = postProcess("".join(res2))

print("Promql Query 2 ==>", res2)
