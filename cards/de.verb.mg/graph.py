def graph():
    for line in LINKS.splitlines()[1:]:
        de, en = line.split("--")
        de = de.strip()
        en = en.split("#")[0].strip()
        yield ("de.verb", en, de)

LINKS = """de -- en                                     # notes (ignored)
sein          -- to be                                  # aux
haben         -- to have                                # aux
werden        -- to become, to will                     # aux, and modal?
können        -- to can                                 # modal
müssen        -- to must                                # modal
sollen        -- to should/ought                        # modal
wollen        -- to want                                # modal
dürfen        -- to may                                 # modal
mögen         -- to like                                # modal
sagen         -- to say
machen        -- to make/do
geben         -- to give
kommen        -- to come
gehen         -- to go
wissen        -- to know
sehen         -- to see
lassen        -- to let/allow, to have done
stehen        -- to stand
finden        -- to find
bleiben       -- to stay (at)
liegen        -- to lie (down)
heißen        -- to hail/be called
denken        -- to think
nehmen        -- to take
tun           -- to do/perform
glauben       -- to believe
halten        -- to halt, to hold
nennen        -- to name
zeigen        -- to show
führen        -- to lead
sprechen      -- to speak
bringen       -- to bring, to take
leben         -- to live (alive)
fahren        -- to go, to ride, to drive, ...
meinen        -- to think/opine
fragen        -- to ask
kennen        -- to know
gelten        -- to be valid (not expired)
stellen       -- to set/place
spielen       -- to play
arbeiten      -- to work
brauchen      -- to require/need
folgen        -- to follow
lernen        -- to learn
bestehen      -- to exist, to insist, to pass (an exam) # be+stehen
verstehen     -- to understand                          # ver+stehen
setzen        -- to set/place
bekommen      -- to get/receive                         # be+kommen
beginnen      -- to begin
erzählen      -- to tell                                # er + zählen
versuchen     -- to try/attempt                         # ver + suchen
schreiben     -- to write
laufen        -- to walk
erklären      -- to explain                             # er + klären
entsprechen   -- to correspond                          # ent + sprechen
sitzen        -- to sit
ziehen        -- to pull/move
scheinen      -- to shine, to seem/appear
fallen        -- to fall
gehören       -- to belong                              # ge + hören?
entstehen     -- to originate/develop, to arise         # ent + stehen
erhalten      -- to receive                             # er + halten
treffen       -- to meet
suchen        -- to search
legen         -- to lay (sth. down)
vorstellen    -- to introduce, to imagine               # vor + stellen
handeln       -- to deal/trade
erreichen     -- to achieve/reach                       # er + reichen
tragen        -- to carry, to wear
schaffen      -- to manage, to create
lesen         -- to read
verlieren     -- to lose                                # ver + lieren?
darstellen    -- to portray/depict                      # dar + stellen
erkennen      -- to admit/recognise
entwickeln    -- to develop                             # ent + wickeln
reden         -- to talk
aussehen      -- to look/appear
erscheinen    -- to appear                              # er + scheinen
bilden        -- to form, to educate
anfangen      -- to begin                               # an + fangen
erwarten      -- to expect                              # er + warten
wohnen        -- to live/reside
betreffen     -- to concern/affect                      # be + treffen
warten        -- to wait
vergehen      -- to pass (time)                         # ver + gehen
helfen        -- to help
gewinnen      -- to win/gain                            # not from winnen?
schließen     -- to close
fühlen        -- to feel
bieten        -- to offer
interessieren -- to interest
erinnern      -- to remind
ergeben       -- to result in
anbieten      -- to offer
studieren     -- to study
verbinden     -- to connect/link
ansehen       -- to watch/look at
fehlen        -- to lack
bedeuten      -- to mean/to represent
vergleichen   -- to compare
möchten       -- to would like                          # modal, K2P of mögen
"""
