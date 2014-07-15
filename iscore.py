#NYCBB convert iScore to TeamPages format

import csv, sys
import math

class Player:
    def __init__(self, NUM, NAME, MIN, FGM, FGA, threePM, threePA, FTM, FTA,
                 OREB, DREB, REB, AST, STL, BLK, TO, PF, CHG, PTS, TEAM):
        #comments are col number corresponding o the iscore csv file in a row
        self.num = NUM #0
        self.name = NAME #1
        self.min = MIN #3
        self.fgm = FGM #4
        self.fga = FGA #5
        self.threepm = threePM #10
        self.threepa = threePA #11
        self.ftm = FTM #13
        self.fta = FTA #14
        self.oreb = OREB #16
        self.dreb = DREB #17
        self.reb = REB #18
        self.ast = AST #19
        self.stl = STL #20
        self.blk = BLK #21
        self.to = TO #23
        self.pf = PF #24
        self.chg = CHG #25
        self.pts = PTS #27
        self.team = TEAM #visitor or home


class TeamPageFormat:
    def __init__(self, output):
        self.text = open(output, "ab")

    def print_top_section(self):
        line = '''<cpi10>
<lpi6>

Official Basketball Box Score -- GAME TOTALS -- FINAL STATISTICS
       vs 
'''

        print >> self.text, line
        print line
    def print_header(self, team_type):
        print team_type
        print >> self.text, team_type+":"
        print "                          TOT-FG  3-PT         REBOUNDS"
        print >> self.text, "                          TOT-FG  3-PT         REBOUNDS"
        print "## Player Name            FG-FGA FG-FGA FT-FTA OF DE TOT PF  TP  A TO BLK S MIN"
        print >> self.text, "## Player Name            FG-FGA FG-FGA FT-FTA OF DE TOT PF  TP  A TO BLK S MIN"
    def print_TEAM_DOTs(self):
        print >> self.text, "   TEAM................."
        print "   TEAM................."

    def print_totals(self, players):
        tot_fg_fg = 0
        tot_fg_fga = 0
        threept_fg = 0
        threept_fga = 0
        ft = 0
        fta = 0
        of = 0
        de = 0
        tot = 0
        pf = 0
        tp = 0
        a = 0
        to = 0
        blk = 0
        s = 0
        min_ = 0 

        for p in players:
            tot_fg_fg += int(p.fgm)
            tot_fg_fga += int(p.fga)
            threept_fg += int(p.threepm)
            threept_fga += int(float(p.threepa))
            if p.threepa < 0:
                print 'p.threepa is negative', p.name, p.threepa
            ft += int(p.ftm)
            fta += int(p.fta)
            of += int(float(p.oreb))
            de += int(p.dreb)
            tot += int(p.reb)
            pf += int(p.pf)
            tp += int(p.pts)
            a += int(float(p.ast))
            to += int(p.to)
            blk += int(p.blk)
            s += int(p.stl)
            min_ += int(p.min)

        tot_fg_fg = str(tot_fg_fg)
        if len(tot_fg_fg) == 1: tot_fg_fg = " " + tot_fg_fg
        tot_fg_fga = str(tot_fg_fga)
        if len(tot_fg_fga) == 1: tot_fg_fga = tot_fg_fga + "  "
        if len(tot_fg_fga) == 2: tot_fg_fga = tot_fg_fga + " "
       
        threept_fg = str(threept_fg)
        if len(threept_fg) == 1: threept_fg = " " +threept_fg
        threept_fga = str(threept_fga)
        if len(threept_fga) == 1: threept_fga = threept_fga + "  "
        if len(threept_fga) == 2: threept_fga = threept_fga + " "

        ft = str(ft)
        if len(ft) == 1: ft = " " + ft
        fta = str(fta)
        if len(fta) == 1: fta = fta + "  "
        if len(fta) == 2: fta = fta + " "

        of = str(of)
        if len(of) == 1: of = " " + of

        de = str(de)
        if len(de) == 1: de = " " + de

        tot = str(tot)
        if len(tot) == 1: tot = "  " + tot + " "
        if len(tot) == 2: tot = tot + " "

        pf = str(pf)
        if len(pf) == 1: pf = " " + pf
      
        tp = str(tp)
        if len(tp) == 1: tp = "  " + tp
        if len(tp) == 2: tp = " " + tp
        
        a = str(a)
        if len(a) == 1: a = " " + a

        to = str(to)
        if len(to) == 1: to = " " + to

        blk = str(blk)
        if len(blk) == 1: blk = " " + blk + " "
        if len(blk) == 2: blk = " " + blk

        s = str(s)
        min_ = str(min_)
        if len(min_) == 1: min_ = " " + min_ + " "
        if len(min_) == 2: min_ = " " + min_

        line = " ".join(["   Totals............... ",
               tot_fg_fg+"-"+tot_fg_fga,
               threept_fg+"-"+threept_fga,
               ft+"-"+fta,
               of, 
               de, 
               tot, 
               pf, 
               tp, 
               a, 
               to, 
               blk, 
               s, 
               min_
               ])
        
        print >> self.text, line
        print line

    def print_percentage(self):
        line = '''TOTAL FG% 1st Half:           %   2nd Half:           %   Game:     %  DEADB
3-Pt. FG% 1st Half:           %   2nd Half:           %   Game:     %   REBS
F Throw % 1st Half:           %   2nd Half:           %   Game:     %    '''
        print >> self.text, line
        print line

    def print_officials(self):
        line = '''Officials:
Technical fouls: 
Attendance: 
Score by Periods                1st  2nd   Total
Santa Ana Dons................            -     
Fullerton Hornets.............            -     '''
        print >> self.text, line
        print line

    def print_separate(self):
        print >> self.text, "--------------------------------------------------------------------------------"
        print "--------------------------------------------------------------------------------"

    def print_player(self, player):
        num = str(player.num)
        if len(num) == 1: num += " "

        name = player.name
        name_space = 21
        dot_needed = name_space - len(name)
        name += '.' * dot_needed

        fg = str(player.fgm)
        fga = str(player.fga)
        if len(fga) == 1: fga += "  "
        if len(fga) == 2: fga += " "

        fg_ = str(player.threepm)
        if len(fg_) == 1: fg_ = " " + fg_
        fga_ = str(player.threepa)
        if len(fga_) == 1: fga_ += "  "
        if len(fga_) == 2: fga_ += " "

        ft = str(player.ftm)
        if len(ft) == 1: ft = " " + ft
        fta = str(player.fta)
        if len(fta) == 1: fta += "  "
        if len(fta) == 2: fta += " "

        of = str(player.oreb)
        if len(of) == 1: of = " " + of

        de = str(player.dreb)
        if len(de) == 1: de = " " + de

        tot = str(player.reb)
        if len(tot) == 1: tot = " " + tot

        pf = str(player.pf)
        if len(pf) == 1: pf = "  " + pf

        tp = str(player.pts)
        if len(tp) == 1: tp = "  " + tp
        if len(tp) == 2: tp = " " + tp

        a = str(player.ast)
        if len(a) == 1: a = " " + a

        to = str(player.to)
        if len(to) == 1: to = " " + to

        blk = str(player.blk)
        if len(blk) == 1: blk = " " + blk

        s = str(player.stl)
        if len(s) == 1: s = " " + s

        min_ = str(player.min)
        min_ = " " + min_
        line = ' '.join([num,
                 name, " ", # add star? 
                 fg+"-"+fga,
                 fg_+"-"+fga_,
                 ft+"-"+fta,
                 of,
                 de,
                 tot,
                 pf,
                 tp,
                 a,
                 to,
                 blk,
                 s,
                 min_]
                 )
        print line
        print >> self.text, line
    
def is_old_header(csvfile):
    f = open(csvfile, "rb")
    r = csv.reader(f).next()
    if len(r) == 28: #up to 'AB' column
        return True
    if len(r) == 24: #up to 'Z' column
        return False
    else:
        print 'HEADER LENGTH NOT SUPPORTED'
        #else: we should exist here if iscore change again...

def build_players(csvfile, team):
    players = []
    f = open(csvfile, "rb")
    for index, r in enumerate(csv.reader(f)):
        if index <1: continue
        if r[1].strip() == "TEAM": break
        if r[1].strip() == "TOTALS": break

        if is_old_header(csvfile):
            print 'old hearder'
            p = Player(r[0], r[1].strip(), r[3], r[4], r[5], r[10], r[11], r[13], r[14], r[16],
                   r[17], r[18], r[19], r[20], r[21], r[23], r[24], r[25], r[27], team)
        else:
            #homestats(53).csv
            print 'new hearder'
            p = Player(r[0], r[1].strip(), r[3], r[4], r[5], r[8], r[9], r[10], r[11], r[12], r[13], 
                       r[14], r[15], r[16], r[17], r[19], r[20], r[21], r[23], team)
        
        players.append(p)

##    for player in players:
##        print "\n"
##        for attr, value in player.__dict__.iteritems():
##            print attr, value, "--",

    return players

def main(visitor_file, home_file):
    visitor_team = build_players(visitor_file, "visitor")
    home_team = build_players(home_file, "home")
    tp = TeamPageFormat("/tmp/result.txt")

    tp.print_top_section()
    tp.print_separate()

    tp.print_header("VISITORS")
    for player in visitor_team:
        tp.print_player(player)

    tp.print_TEAM_DOTs()
    tp.print_totals(visitor_team)
    tp.print_percentage()
    tp.print_separate()

    tp.print_header("HOME TEAM")
    for player in home_team:
        tp.print_player(player)
    tp.print_TEAM_DOTs()
    tp.print_totals(home_team)
    tp.print_percentage()
    tp.print_separate()

    tp.print_officials()

if __name__ == "__main__":
    main("visitor.csv", "home.csv")
