#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 03.03.2016
#@author: Alex Ferechin
#@contact: alex.ferechin@gmail.com

import random
from route5.models import db_code5

def _is_free(code5):
    return True

def _is_reserved(code5):
    return True

def generate_pool():
    pass

def get_next_code5():
    '''
    db.collection.findAndModify({
      query: { _id: "some potentially existing id" },
      update: {
        $setOnInsert: { foo: "bar" }
      },
      new: true,   // return new doc if one is upserted
      upsert: true // insert the document if it does not exist
    })

    find_and_modify(query={}, update=None, upsert=False, sort=None, full_response=False, manipulate=False, **kwargs)¶

    '''
    while True:
        code5 = [str(random.randrange(0, 255)) for x in xrange(5)]
        str_code5 = "".join(["0"*(3-len(x))+x for x in code5])
        code5 = int(str_code5)
        obj = db_code5.find_one({"_id": code5})
        if obj:
            continue
        db_code5.save({"_id":code5, "is_booked": 1, "code5": str_code5})
        break
    str_code5 = "%s-%s-%s-%s-%s" % (str_code5[:3], str_code5[3:6], str_code5[6:9], str_code5[9:12], str_code5[12:16])
    return code5, str_code5


def get_str_code5(code5):
    str_code5 = "0"*(15 - len(str(code5))) + str(code5)

    return "%s-%s-%s-%s-%s" % (str_code5[:3], str_code5[3:6], str_code5[6:9], str_code5[9:12], str_code5[12:16])

def check_code5():
    pass

def code5_to_address():
    pass

def address_to_code5():
    pass

def is_valid_promotion(promotion):
    return False