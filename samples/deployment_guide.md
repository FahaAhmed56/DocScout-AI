# Deployment Guide

Deployments must pass automated tests before release.

Production secrets should live in environment variables, not source control.

For a rollback, restore the last known working version and inspect service logs.
