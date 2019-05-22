#!/bin/bash
papermill update_github_stats.ipynb s3://python-portfolio-notebooks/saved-github-notebooks/"$(date +"%m-%d-%y")".ipynb
