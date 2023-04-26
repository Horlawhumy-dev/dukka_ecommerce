#!/bin/bash

autopep8 --in-place --aggressive --aggressive ./*.py ./dukka_ecommerce/dukka_ecommerce/*.py
autoflake --in-place --remove-unused-variables ./*.py ./dukka_ecommerce/dukka_ecommerce/*.py
black ./
isort ./