#!/usr/bin/env python3

# Streaker
# Copyright 2013 Meadow Hill Software
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random
import time

dates = {}
questions = {}
answers = {}
times = {}
priorities = []
hand = {}

def loadCards():
	global flash
	global dates
	global questions
	global answers
	global times
	global blah
	global unformatted
	flash = input("\nEnter the name of your flash card file: ")
	flashcards = open(flash, "r")
	dateKey = 0
	questionKey = 0
	answerKey = 0
	timeKey = 0
	while True:
		part = flashcards.readline()
		if not part:
			break
		if part[0] == "!":
			part = part[1: (len(part) - 2)]
			d = part[:]
			dates[dateKey] = d
			dateKey += 1
		elif part[0] == "?":
			part = part[1:(len(part) - 2)]
			question = part[:]
			questions[questionKey] = question
			questionKey += 1
		elif part[0] == "@":
			part = part[1:(len(part) - 2)]
			answer = part[:]
			answers[answerKey] = answer
			answerKey += 1
		elif part[0] == "-":
			part = part[1:(len(part) - 2)]
			time = part[:]
			times[timeKey] = time
			timeKey += 1
		else:
			if part != "":
				blah = "q"
				unformatted = 1
				break
	flashcards.close()
	if blah != "q":
		Qs = len(questions)
		As = len(answers)
		Ts = len(times)
		Ds = len(dates)
		if Qs != As:
			blah = "q"
			unformatted = 1
			print("The number of questions in the flash card file does not match the number of answers in the file.")
		else:
			while Ts < Qs:
				times[Ts] = "0"
				Ts += 1
			while Ds < Qs:
				dates[Ds] = str(date)
				Ds += 1

def test():
	global blah
	global memorized
	global priorities
	global times
	hand = {}
	Ts = sorted(times)
	key = 0
	while hand == {}:
		for T in Ts:
			if int(times[T]) <= date:
				if dates[T] == priorities[0]:
					hand[key] = T
					key += 1
		if hand == {}:
			priorities.remove(priorities[0])
			priorities.sort()
	key = random.randint(0, (len(hand) - 1))
	question = questions[hand[key]]
	answer = answers[hand[key]]
	blah = input(("\n" + question + " (Press 'Enter' to see the answer.)"))
	if blah.lower() not in q:
		print("\n" + answer)
		print("\n~Options~\n0: Keep asking me.\n1: Ask me again tomorrow.\n2: Ask me again in two days.\n3: Ask me again in three days.\n4: Ask me again in one week.")
		global memory
		memory = "~"
		while memory not in ["0", "1", "2", "3", "4", "q", "quit"]:
			memory = input("\nEnter your selection: ")
		if memory in ["1", "2", "3", "4"]:
			if memory == "4":
				newDay = day + 7
			if memory != "4":
				newDay = day + int(memory)
			if newDay > days[month]:
				newDay = newDay - days[month]
				newMonth = month + 1
				if newMonth > 12:
					newMonth = 1
					newYear = year + 1
				else:
					newYear = year
			elif newDay <= days[month]:
				newMonth = month
				newYear = year
			newMonth = str(newMonth)
			if len(newMonth) == 1:
				newMonth = "0" + newMonth
			newDay = str(newDay)
			if len(newDay) == 1:
				newDay = "0" + newDay
			time = str(newYear) + newMonth + newDay
			times[hand[key]] = time
			memorized += 1

date = int(time.strftime("%Y%m%d"))
stringYear = time.strftime("%Y")
two = int(stringYear[2:4])
year = int(stringYear)
month = int(time.strftime("%m"))
day = int(time.strftime("%d"))
leaps = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 88, 92, 96]
days = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
if two in leaps:
	days[2] = 29

blah = ""
memory = ""
print("Enter 'quit' at any time to exit the program.")
q = ["q", "quit"]
memorized = 0
unformatted = 0
flash = "flash.txt"

loadCards()

timeList = sorted(times)

for key in timeList:
	if int(times[key]) > date:
		memorized += 1

Ds = sorted(dates)
for D in Ds:
	if dates[D] not in priorities:
		if int(times[D]) <= date:
			priorities.append(dates[D])
priorities.sort()

while blah.lower() not in q and memory.lower() not in q and memorized < len(times):
	test()
	
if memorized == len(times):
	print("\nYou've memorized all the cards in the deck.")

if unformatted == 0:
	flashcards = open(flash, "w")
	for key in timeList:
		flashcards.write("!" + dates[key] + "!\n")
		flashcards.write("?" + questions[key] + "?\n")
		flashcards.write("@" + answers[key] + "@\n")
		flashcards.write("-" + times[key] + "-\n")
	flashcards.close()
