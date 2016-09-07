#! /usr/bin/env python3

from getFAH import readSV,writeSV

def main():
    data = readSV('score.psv')
    scoreList = []
    for line in data:
        scoreList.append(int(line[-1]))
    scoreList.sort()
    scoreList.reverse()
    for line in data:
        line.append(str(scoreList.index(int(line[-1]))))
    writeSV('rank.psv',data)

if __name__ == '__main__':
    main()