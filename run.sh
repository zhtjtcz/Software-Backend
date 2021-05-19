#!/bin/bash
a=(`ps -ef | grep "runserver" | awk '{print $2}'`)
b=(`ps -ef | grep "runserver" | awk '{print $14}'`)
echo $a
echo $b