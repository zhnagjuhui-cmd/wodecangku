#!/usr/bin/env python3
# coding: utf-8
"""Explicitly reopen a blocked page without erasing its queue or dispatch history."""
import argparse
from slide_run_state import deck_dir_from_target, find_slide, locked_jobs, now_iso, update_jobs_run_status, set_run_status


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('deck')
    p.add_argument('--slide',required=True)
    p.add_argument('--reason',required=True)
    p.add_argument('--agent-id',help='Original agent id when its dispatch is being resumed')
    p.add_argument('--reassign',action='store_true',help='Explicitly return to pending for a newly dispatched worker')
    a=p.parse_args()
    deck=deck_dir_from_target(a.deck)
    with locked_jobs(deck) as jobs:
        slide=find_slide(jobs,a.slide)
        if slide['status']!='blocked':
            raise SystemExit('Only blocked pages may be reopened')
        old=slide.get('dispatch')
        if old and not a.reassign and a.agent_id!=old.get('agent_id'):
            raise SystemExit('Resuming a dispatch requires the original agent id, or explicit --reassign')
        slide.setdefault('recovery_history',[]).append({'time':now_iso(),'reason':a.reason,
                                                       'blocker':slide.get('blocker'),'dispatch':old})
        slide['blocker']=None
        slide['status']='pending' if a.reassign or not old else 'dispatched'
        if a.reassign:
            slide['dispatch']=None
        jobs['run_status']='resuming'
        update_jobs_run_status(jobs)
        state=slide['status']
    set_run_status(deck,'resuming','reopened '+a.slide+' without changing image queue')
    print(a.slide+' -> '+state)


if __name__=='__main__':
    main()
