import sys
import time
import traceback
from datetime import datetime

import pytz
import rulez
import transaction
from celery.app.task import Context
from celery.result import AsyncResult
from morpfw.signal.signal import (
    TASK_COMPLETED,
    TASK_FAILED,
    TASK_FINALIZED,
    TASK_STARTING,
    TASK_SUBMITTED,
)

from ..app import App


@App.subscribe(model=AsyncResult, signal=TASK_SUBMITTED)
def task_submitted(app, request, context, signal):
    now = datetime.now(tz=pytz.UTC)
    col = request.get_collection("morpcc.process")
    res = col.search(rulez.field["task_id"] == context.id)
    if not res:
        col.create(
            {
                "task_id": context.id,
                "start": now,
                "signal": context.__signal__,
                "params": context.__params__,
            },
            deserialize=False,
        )
    print("task %s submitted" % context.id)


@App.subscribe(model=Context, signal=TASK_STARTING)
def task_starting(app, request, context, signal):
    proc = None
    for retry in range(5):
        col = request.get_collection("morpcc.process")
        res = col.search(rulez.field["task_id"] == context.id)
        if res:
            proc = res[0]
            break
        print("Process Manager for Task %s is not ready" % context.id)
        time.sleep(5)
    if proc is None:
        print(
            "Unable to locate Process Manager for Task %s, "
            "proceeding without tracking" % context.id
        )
    else:
        sm = proc.statemachine()
        sm.start()
        transaction.commit()
        request.clear_db_session()
        transaction.begin()

    print("Task %s starting" % context.id)


@App.subscribe(model=Context, signal=TASK_COMPLETED)
def task_completed(app, request, context, signal):
    col = request.get_collection("morpcc.process")
    res = col.search(rulez.field["task_id"] == context.id)
    if res:
        proc = res[0]
        sm = proc.statemachine()
        sm.complete()
        transaction.commit()
        request.clear_db_session()
        transaction.begin()

    print("Task %s completed" % context.id)


@App.subscribe(model=Context, signal=TASK_FAILED)
def task_failed(app, request, context, signal):
    col = request.get_collection("morpcc.process")
    res = col.search(rulez.field["task_id"] == context.id)
    if res:
        proc = res[0]
        sm = proc.statemachine()
        sm.fail()
        tb = traceback.format_exc()
        proc["traceback"] = tb
        transaction.commit()
        request.clear_db_session()
        transaction.begin()

    print("Task %s failed" % context.id)


@App.subscribe(model=Context, signal=TASK_FINALIZED)
def task_finalized(app, request, context, signal):
    pass
