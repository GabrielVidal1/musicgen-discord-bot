#!/bin/bash
env $(cat .env | xargs) python3 main.py