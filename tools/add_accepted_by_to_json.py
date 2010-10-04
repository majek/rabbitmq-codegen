#!/usr/bin/env python
import libxml2
import sys


doc = libxml2.parseFile("amqp-0-9-1.xml")
ctxt = doc.xpathNewContext()
nodes = ctxt.xpathEval("//method/chassis")

all_options = set()
dd = {}
for chas in nodes:
    m = chas.parent
    c = m.parent
    cidx, midx = int(c.prop('index')), int(m.prop('index'))
    if cidx not in dd: dd[cidx] = {}
    if midx not in dd[cidx]: dd[cidx][midx] = []
    dd[cidx][midx].append( chas.prop('name') )
    all_options.add( chas.prop('name') )

doc.freeDoc()
ctxt.xpathFreeContext()

import simplejson as json

j = json.loads(file("../amqp-rabbitmq-0.9.1.json").read())

for c in j["classes"]:
    for m in c['methods']:
        cidx, midx = c['id'], m['id']
        if cidx in dd and midx in dd[cidx]:
            m['accepted-by'] = dd[cidx][midx]
        else:
            print >> sys.stderr, "NOT SUPPORTED: %s %s" % (c['name'], m['name'])
            m['accepted-by'] = list(all_options)

print json.dumps(j, indent=4).replace(" \n", "\n")

