import asyncio
import json

import httpx
import datetime
from dateutil.relativedelta import relativedelta


class GitIssue():
    """
    Git Issues工具类
    """
    def __init__(self):
        self._git = httpx.AsyncClient(http2=True, verify=False, proxies=None)
        self._host = "https://api.github.com"
        self._git_stander_header = {"Accept": "application/vnd.github.v3+json",
                                    "Authorization": ""}

    async def list_repo_issues(self, owner: str, repo: str, labels: list, since: str = None) -> json:
        repo_issue_url = f"{self._host}/repos/{owner}/{repo}/issues"
        issue_params = {"sort": "created", "state": "open", "per_page": "100"}
        if labels: issue_params.update({"labels": ','.join(label for label in labels)})
        if since: issue_params.update({"since": since})
        response = await self._git.get(url=repo_issue_url, headers=self._git_stander_header, params=issue_params)
        return json.loads(response.content.decode("utf-8"))

    async def list_multi_repo_issues(self, repo_list: list) -> list:
        """
        multi 查询仓库issues
        :param repo_list:
        :return: 结果顺序与传入相同
        """
        task_list = []
        for repo in repo_list:
            task = asyncio.create_task(self.list_repo_issues(repo['owner'], repo['repo'], repo['labels'], repo['since']))
            task_list.append(task)
        results = await asyncio.gather(*task_list)
        return list(results)

    @staticmethod
    def _relative_iso_time(years=0, months=0, weeks=0, days=0) -> str:
        """
        相对时间转ISO工具
        :param years: 年
        :param months: 月
        :param weeks: 周
        :param days: 天
        :return: ISO格式时间
        """
        return relative_time(years=years, months=months, days=days, weeks=weeks).isoformat()


# 相对日期工具
def relative_time(use_now=True, date_string=None, date_format=None, years=0, months=0, days=0,
                  weeks=0, hours=0, minutes=0, seconds=0, microseconds=0) -> datetime.datetime:
    relative_delta = relativedelta(years=years, months=months, days=days, weeks=weeks, hours=hours,
                                   minutes=minutes, seconds=seconds, microseconds=microseconds)
    _date = datetime.datetime.now() if use_now else datetime.datetime.strptime(date_string, date_format)
    return _date + relative_delta


if __name__ == "__main__":
    body = [{"owner": "vuejs", "repo": "vue", "labels": ['bug'], "since": ''}]
    git = GitIssue()
    con = asyncio.run(git.list_multi_repo_issues(body))
    print(con)
