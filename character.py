# character.py

import random
import util

ranks = {
	"cadet" : (0.9, 0),
	"ensign" : (1.1, 0.5),
	"ltjg" : (1.15, 1),
	"lt" : (1.2, 1.5),
	"ltcmdr" : (1.25, 2),
	"cmdr" : (1.3, 2.5),
	
	"crewman" : (0.9, 0),
	"jpo" : (0.95, 0.25),
	"po" : (1, 0.5),
	"cpo" : (1.1, 1),
	"scpo" : (1.2, 1.5),
	"mcpo" : (1.25, 2)
	}
	
enlisted = (
		"crewman",
		"jpo",
		"po",
		"cpo",
		"scpo",
		"mcpo"
	)
	
officer = (
		"cadet",
		"ensign",
		"ltjg",
		"lt",
		"ltcmdr",
		"cmdr"
	)

rank_titles = {
	"cadet" : "Cadet",
	"ensign" : "Ensign",
	"ltjg" : "Lieutenant Junior Grade",
	"lt" : "Lieutenant",
	"ltcmdr" : "Lieutenant Commander",
	"cmdr" : "Commander",
	
	"crewman" : "Crewman",
	"jpo" : "Junior Petty Officer",
	"po" : "Petty Officer",
	"cpo" : "Chief Petty Officer",
	"scpo" : "Senior Chief Petty Officer",
	"mcpo" : "Master Chief Petty Officer"
}

class Character(object):
    def __init__(self, name, tac = 0, sec = 0,\
    	ops = 0, eng = 0, sci = 0, med = 0, cmd = 0, rank = "cadet", ver = 0):
        self.name = name
        self.tac = tac
        self.sec = sec
        self.ops = ops
        self.eng = eng
        self.sci = sci
        self.med = med
        self.cmd = cmd
        self.rank = rank
        self.ver = ver

    def _calc(self, skill, rand):
        if self.ver == 0:
            return 2*skill*rand*ranks[self.rank][0]
        else:
            return (2*skill*rand) + ranks[self.rank][1]

    def check(self, skill):
        if skill == "tac":
            return self._calc(self.tac, random.random())
        elif skill == "sec":
            return self._calc(self.sec, random.random())
        elif skill == "ops":
            return self._calc(self.ops, random.random())
        elif skill == "eng":
            return self._calc(self.eng, random.random())
        elif skill == "sci":
            return self._calc(self.sci, random.random())
        elif skill == "med":
            return self._calc(self.med, random.random())
        elif skill == "cmd":
            return self._calc(self.cmd, random.random())
        else:
            return self._calc(0, 0)
            
    def upgrade(self):
        if self.max_stars >= 10:
            return False
        
        skills = (
        	    self.check("tac"),
        	    self.check("sec"),
        	    self.check("ops"),
        	    self.check("eng"),
        	    self.check("sci"),
        	    self.check("med"),
        	    self.check("cmd")
        	  )
        
        winner = skills.index(max(skills))
        
        if winner == 0:
            self.tac += 1
            return "tac", self.tac
        elif winner == 1:
            self.sec += 1
            return "sec", self.sec
        elif winner == 2:
            self.ops += 1
            return "ops", self.ops
        elif winner == 3:
            self.eng += 1
            return "eng", self.eng
        elif winner == 4:
            self.sci += 1
            return "sci", self.sci
        elif winner == 5:
            self.med += 1
            return "med", self.med
        elif winner == 6:
            self.cmd += 1
            return "cmd", self.cmd
        else:
            raise Exception("Inconceivable!")
    
    def promote(self):
        if self.rank in ("mcpo", "cmdr"):
            return False
        
        elif self.rank in enlisted:
            self.rank = enlisted[ enlisted.index(self.rank) + 1 ]
        
        elif self.rank in officer:
            self.rank = officer[ officer.index(self.rank) + 1 ]
    
        else:
            self.rank = "crewman"
        
        return self.rank

    def lead(self, stat, team):
        personal = self.check(stat)

        results = [crew.check(stat) for crew in team]

        command_limit = int(max((self.command_limit, personal)))
        
        results = util.max_elements(results, command_limit)
        results += (personal,)
    
        return sum(results)

    @property
    def command_limit(self):
        return int(self.cmd * ranks[self.rank][1])
            
    @property
    def stars(self):
        total = self._calc(self.tac, 1) +\
            self._calc(self.sec, 1) +\
            self._calc(self.ops, 1) +\
            self._calc(self.eng, 1) +\
            self._calc(self.sci, 1) +\
            self._calc(self.med, 1) +\
            self._calc(self.cmd, 0.5)
        return min(total / 6.5, 10.0)
    
    @property
    def max_stars(self):
        temp = self.rank
        
        if temp in enlisted:
            self.rank = "mcpo"
        else:
            self.rank = "cmdr"
        
        stars = self.stars
        self.rank = temp
        
        return stars

    @property
    def stats(self):
        return {
            "tac" : self.tac,
            "sec" : self.sec,
            "ops" : self.ops,
            "eng" : self.eng,
            "sci" : self.sci,
            "med" : self.med,
            "cmd" : self.cmd
        }
        
    def __str__(self):
        return " ".join((rank_titles[self.rank], self.name))

    def __repr__(self):
        if self.rank in ("mcpo", "cmdr"):
            return "".join(("< ", str(self), " ", str(round(self.stars, 1)),\
                            "★ >"))
        return "".join(("< ", str(self), " ", str(round(self.stars, 1)),\
                        "/", str(round(self.max_stars, 1)), "★ >"))

# Default Characters
kim = Character("Harry Kim",5,2,6,2,1,1,2,"ensign")
obrien = Character("Miles O'Brien",4,2,6,7,1,1,4,"scpo")
tuvok = Character ("Tuvok",6,5,3,2,1,1,6,"ltcmdr")

# Statistics
suffer = [obrien for i in range(100)]

def min_lead(leader, stat = "eng", team = None, count = 100):
    if team is None:
        team = suffer
    total = 666
    for i in range(count):
        result = leader.lead(stat, team)
        if result < total:
            total = result
    return total

def max_lead(leader, stat = "eng", team = None, count = 100):
    if team is None:
        team = suffer
    total = 0
    for i in range(count):
        result = leader.lead(stat, team)
        if result > total:
            total = result
    return total

def avg_lead(leader, stat = "eng", team = None, count = 100):
    if team is None:
        team = suffer
    total = 0
    for i in range(count):
        total += leader.lead(stat, team)
    return total/count
