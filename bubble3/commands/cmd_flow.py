# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.
from collections import deque

import click
import time 

from ..cli import pass_bubble
from ..cli import STAGES

from ..util.store import get_bubble
from ..util.remember import add_line_to_file,del_file
from ..util.zipit import zipit
from ..util.generators import get_gen_slice
from ..util.cli_misc import bubble_lod_dump, bubble_lod_load
from ..util.counter import Counter
from ..util.cli_misc import update_stats, make_uniq_for_step
from ..util.cli_misc import get_client, update_stats
from ..transformer import Transformer

from ..cli import pass_bubble
from ..cli import STAGES

def get_client_ready(ctx,CCFG):
    clientmod=get_client(ctx.gbc, CCFG.CLIENT, ctx.home)
    try:
        client = clientmod.BubbleClient(cfg=CCFG)
        client.set_parent(ctx.gbc)
        client.set_verbose(ctx.get_verbose())
        return client
    except Exception as e:
        ctx.say_red(
            'cannot create bubble client:' + CCFG.CLIENT)
        ctx.say_red(str(e))
        raise click.Abort('cannot perform pull/push action on client')

#def do_yielding_transform(ctx, transformer, to_transform, total_counter, error_counter):
def do_transform(ctx, transformer, data, total_counter, error_counter):
 ctx.say('do_transform',stuff=(ctx, transformer, data, total_counter, error_counter))
 total_counter.count()
 try:
  res = transformer.transform(data)
 except Exception as excpt:
  res = {'exception': str(excpt)}
  return res
 #if 'BUBBLE_SKIPPING' in res:
 #   pass #:continue
 if 'BUBBLE_ERROR' in res:
  error_counter.count()
 if 'exception' in res:
  error_counter.count()
 if 'BUBBLE_SKIPPING' not in res:
  return res


def get_transformer(ctx,stage,path):
    """Transform data"""
    ctx.say('transform',stuff=(ctx,stage,path))
    TRANSFORM = ctx.cfg.CFG[stage].TRANSFORM
    RULES = TRANSFORM.RULES
    stored = bubble_lod_load(ctx, 'store', stage)
    try: stored_data = next(stored)
    except StopIteration:stored_data={}
    
    ctx.gbc.say('stored:', stuff=stored_data, verbosity=150)

    cfgdict = {}
    cfgdict['CFG'] = ctx.cfg.CFG
    cfgdict['GENERAL_BUBBLE_CONTEXT'] = ctx.GLOBALS['gbc']
    cfgdict['ARGS'] = {'stage': stage,
                       'path': path}

    #if type(RULES) == str and RULES.endswith('.bubble'):
    td={}

    td['rules']=get_bubble(ctx.gbc, path + RULES)
    td['rule_type']='bubble'
    td['store']=stored_data
    td['config']=cfgdict
    td['bubble_path']=path
    td['verbose']=ctx.get_verbose()
    transformer = Transformer(**td)

    transformed_count = Counter()
    error_count = Counter()
    #yield do_yielding_transform(ctx,  #generate a generator?//
    def _transformer(data):
        return do_transform(ctx,
                     transformer,
                     data,
                     transformed_count,
                     error_count)
    return _transformer

def genflow(ctx,stage,puller,transformer,pusher):
    pullfd=del_file(ctx,stage,'pulled')
    pushfd=del_file(ctx,stage,'push')
    pushedfd=del_file(ctx,stage,'pushed')
    for d in puller():
        ctx.say(d)
        #yield 'pull', d
        pullf=add_line_to_file(ctx,stage,'pull',d)
        t=transformer(d)
        #yield 'transform', t
        pushf=add_line_to_file(ctx,stage,'push',t)
        p=pusher(t)
        #yield 'push', p
        pushedf=add_line_to_file(ctx,stage,'pushed',p)
    zipit(ctx,pullf)
    zipit(ctx,pushf)
    zipit(ctx,pushedf)


@click.command('flow', short_help='Pull, Transform, Push, in a flow of events(arrows)(target).')
@click.option ('--amount', '-a', type=int, default=-1, help='set the amount to pump')
@click.option ('--index', '-i', type=int, default=-1, help='set the starting index')
@click.option ('--select', '-f', type=int, default=-1, help='set the select')
@click.option ('--report', '-r', type=int, default=-1, help='set the report')
@click.option ('--stage', '-s', default='DEV', help='set the staging :' + ','.join(STAGES))
@pass_bubble
def cli(ctx, amount, index, select, report, stage):
    """Pull, Transform, Push,streaming inside a flow of data,aka small information filter and fitter in the middle"""
    #initial version is mostly just the "happy flow"
    ctx.say_green("flow: ",stuff=(amount, index, select, report, stage))
    path = ctx.home + '/'
    #STAGE = None
    STAGE = ctx.cfg.CFG[stage]
    SRC = None
    RULES = None
    UNIQ_KEYS_PULL = None
    UNIQ_KEYS_PUSH = None
    CLEAN_MISSING_AFTER_SECONDS = None
    TGT = None
    transformed = True

    #pull(g=globals(),l=locals())
    SRC = STAGE.SOURCE
    TGT = STAGE.TARGET
    src_client = get_client_ready(ctx,SRC) 
    transformer=get_transformer(ctx, stage,path) #just add single data entry as arg
    tgt_client=get_client_ready(ctx,TGT) 
    
    pipe=genflow(ctx,stage,src_client.pull,transformer,tgt_client.push)

