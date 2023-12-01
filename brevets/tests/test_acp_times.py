"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

import nose    # Testing framework
import logging
import arrow
import acp_times as acp

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

start =  arrow.now()
brevet = 1000

#class SimpleTestCases:
    # to test the basic cases fuction as expected
def test_200_int():
    # test when input is an int
    assert acp.open_time(200, brevet, start) == start.shift(hours=5, minutes=53)
    assert acp.close_time(200, brevet, start) == start.shift(hours=13, minutes=20)

def test_200_float():
    # test when input is a float
    assert acp.open_time(200.0, brevet, start) == start.shift(hours=5, minutes=53)
    assert acp.close_time(200.0, brevet, start) == start.shift(hours=13, minutes=20)

#class MultiStepTestCases:
def test_open():
    # 2 rows of table, 200/34 + 100/32
    assert acp.open_time(300.0, brevet, start) == start.shift(hours=9)
    # 4 rows of table, 200/28 + 200/30 + 200/32 + 200/34 
    assert acp.open_time(800.0, brevet, start) == start.shift(hours=25, minutes=57)

def test_close():
    # 4 rows of table, 200/11.428 + 200/15 + 200/15 + 200/15 (or 200/11.428+600/15)
    assert acp.close_time(800.0, brevet, start) == start.shift(hours=57, minutes=30)
    # 2 rows of table, 200/15 + 100/15 (or 300/15)
    assert acp.close_time(300.0, brevet, start) == start.shift(hours=20)
        
#class TestNullCase:
def test_0():
    # test onen/close with 0km control
    assert acp.open_time(0.0, brevet, start) == start
    # since 0 < 60, this control is relaxed, so min 1hr before close
    assert acp.close_time(0.0, brevet, start) == start.shift(hours=1)

# Writing at least 2 (more?) correct tests using nose
#  (put them in tests, follow Project 3 if necessary), 
# and all should pass.

# test submitting a brevet

# test displaying a brevet