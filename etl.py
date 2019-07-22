from prefect import Flow, task
from prefect.schedules import CronSchedule
import datetime


@task
def update_github_stats():

    now = datetime.datetime.now()
    pm.execute_notebook(
        "update_github_Stats.ipynb",
        "s3://python-portfolio-notebooks/github/"
        + str(now.year)
        + "-"
        + str(now.month)
        + "-"
        + str(now.day)
        + ".ipynb",
    )


with Flow("ETL", schedule=CronSchedule("0 9 * * *")) as flow:
    update_github_stats = update_github_stats()

if __name__ == "__main__":
    flow.run()
