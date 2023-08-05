from __future__ import division, print_function
import numpy as np
from . import course, assessment, problemset, section, mathlib
from course import Course
from assessment import Assessment
name = "examsage" # <---- Placing this line between the __future__ import and numpy causes the remaining lines to be ignored for some reason