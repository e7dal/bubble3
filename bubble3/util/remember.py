import json
import os
import signal
import sys
import zipfile
from pathlib import Path

###########################################################

def add_line_to_file(ctx,stage,step,jsonable):
    ffp=ctx.home+'/'+'remember/'+step+'_'+stage+'.jsonl'
    line=json.dumps(jsonable,ensure_ascii=False)+u"\n"
    with open(ffp, 'a') as datafile:
        datafile.write(line)
    return ffp
    
def del_file(ctx,stage,step):
    ffp=ctx.home+'/'+'remember/'+step+'_'+stage+'.jsonl'
    return os.remove(ffp)
#################################################################
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
