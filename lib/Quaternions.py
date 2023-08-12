# Copyright (C) 2023  the-astronot
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see https://www.gnu.org/licenses/.
#
# ________________
# |_File_History_|______________________________________________________________
# |_Programmer______|_Date_______|_Comments_____________________________________
# | the-astronot    | 2023-08-11 | Created File
# |
# |
# |


class Quaternion:
	def __init__(self):
		self.q = [0,0,0,0]

	def __str__(self):
		return "[{0:.4f},{1:.4f},{2:.4f},{3:.4f}]".format(
			self.q[0],self.q[1],self.q[2],self.q[3])
	
	def __repr__(self):
		return self.__str__()
