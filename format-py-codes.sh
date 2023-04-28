#!/bin/bash

autopep8 --in-place --aggressive --aggressive dukka_ecommerce/*.py
autoflake --in-place --remove-unused-variables dukka_ecommerce/*.py
black ./
isort ./