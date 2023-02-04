# -*- coding: utf-8 -*-

# PowerShell trace log command:
# GC -Tail 1 oo.log -Wait

# 스레드를 이용한 비동기 구현 방식

from threading import Thread, Event
from queue import Queue
from datetime import datetime
import sys
import time
import getpass

import workClasses
from workClasses import ManagerInfo
import worksConf
from thefuzz import process
from chromeCrawling import get_chrome_driver


que = None
event = None
confluence_manager_info = None
messenger_manager_info = None


def _get_manager():
    print("관리자 로그인 (업무별 초기 1회 수행)")
    id = input("관리자 계정 ID: ")
    pw = getpass.getpass("관리자 계정 PW: ")
    return id, pw


def get_manager_info(workName: str):
    global confluence_manager_info, messenger_manager_info

    if workName == worksConf.MESSENGER_NAME_KOR:
        if messenger_manager_info is None:
            messenger_manager_info = ManagerInfo(*_get_manager())
        return messenger_manager_info
    elif workName == worksConf.CONFLUENCE_NAME_KOR:
        if confluence_manager_info is None:
            confluence_manager_info = ManagerInfo(*_get_manager())
        return confluence_manager_info


def wait_and_reset(q):
    driver = get_chrome_driver()

    while True:
        if event.is_set():
            break
        if q.qsize() > 0:
            work, workName, managerInfo, userInfo = q.get()
            logPath = work.run(driver, managerInfo, userInfo)

            if logPath == "error":
                continue

            logFile = open(logPath, "a")
            print("[{}] {} : {}님 초기화 완료".format(workName, datetime.now(), userInfo), file=logFile, flush=True)
    driver.quit()


def input_from_user(q):
    workDict = {n: c for n, c in zip(worksConf.WORK_LIST, [workClasses.UCMessenger, workClasses.Confluence])}
    try:
        while True:
            query = sys.stdin.readline()[:-1]

            if "종료" == query:
                event.set()
                return

            if ' ' not in query:
                print("올바른 형식으로 입력해주세요")
                continue

            queryWorkName, userInfo = query.split()

            (workName, similarity) = process.extract(queryWorkName, worksConf.WORK_LIST, limit=1)[0]
            if similarity >= 60:
                work = workDict[workName]()
                managerInfo = get_manager_info(workName)
                q.put((work, workName, managerInfo, userInfo))

                print("{} (입력 값 유사도:{}) 비밀번호 초기화".format(workName, similarity))
            else:
                print("업무명을 다시 입력하세요. 입력값 : {}".format(queryWorkName))

            time.sleep(0.5)
    except:
        event.set()


def main():
    global que, event

    print("업무명과 사용자 정보를 입력해주세요.\n"
          + "예시)\n"
          + "{} [사번]\n".format(worksConf.MESSENGER_NAME_KOR)
          + "{} [메일]\n\n".format(worksConf.CONFLUENCE_NAME_KOR)
          + "종료\n"
          + "--------------------------")

    try:
        que = Queue()
        event = Event()

        workThread = Thread(target=wait_and_reset, args=(que,), daemon=True)
        ioThread = Thread(target=input_from_user, args=(que,))

        workThread.start()
        ioThread.start()
    except:
        workThread.join()
        ioThread.join()


if __name__ == "__main__":
    main()
