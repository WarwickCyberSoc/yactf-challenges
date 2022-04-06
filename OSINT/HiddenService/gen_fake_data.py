import random

usernames="""lividcapture
avariciouscarillon
exxonpug
coventie
cinemapurchase
physicistoppose
adviserdusky
ledgersuccess
hastinesswritable
descentlethargic
suspiciousnerd
minuteevil
colobuslunar
ideaexclaim
nounsquish
historiancorset
sweatythat
peppereddeep
historicshred
scotchtrial
burpgrunt
nonceconflict
intrepidtrail
altruisticreliable
desperatehoe
idlefireplace
rootswedge
haykit
lawlaunch
noxiousattend
jocularlice
authenticpersuade
adviseworry
tauntorder
allegevenezuelan
commitmentspacesuit
formulaankle
ladderdecorate
diesilence
poxsecret
madecane
driproughly
productblock
phonyarrow
cabbagebenefit
affirmstatuesque
speakerpillar
rosemolar
confrontpossessive
growlbusy
chainwisp
buttondownexplore
owelesson
ratlinecynical
catfishswimsuit
standingthick
kimonoincomplete
scandalousfortress
culturevolume
awedsanta
blackstonecourier
bucklehiccup
jackstaytrait
steadplumber
hooliganhorseradish
sinprincipal
patchwatercress
sleuthattractive
journalkimono
tendencybordered
shushguacamole
knockbackfootprints
proposedcranberries
usablecoveralls
corrupthonored
plentyplayoffs
tenteach
flotillaadmired
sandpiperroute
menacingpox
pulloverlooper
lepediscipline
truckcow
mustcrowd
duckboth
tshirttough
diningnearly
candlelightmarmalade
jumpydanone
firminibus
fiddleyuttermost
testedfroze
bearbreathless
couplekissspritsail
barterfellowship
smuthtaunt
tonephoto
belatedweather
indeliblereverence
ceremonywilderness
editionclean
wackyunited
geckovision
senateprocessionary
nauticalclover
marktease
sobavapor
criticallabor
intensityletter
imaginaryripen
budgetterracotta
saxophonestripped
insistsolve
canracing
southeasterlywindbreaker
liquoriceestate
collarwritten
brushlooting
soupintend
layeland
megaprecious
centerbeneficial
wavesonpat
regalhuman
sweetsleap
clevestair
cabotagedoubtful
gloryreputation
umbrellaperpetual
affordharass
pestolonghorn
needfulreceive
pebblegunnage
moccasinsglistening
elementmethodical
flipflopsproperly
rectumfax
encounterarmy
scootslice
callingsternum
welshnebulous
burnishformation
indianalluring
pythonceaseless
cleatsrope
yuletideabject
staleheadsail
rustypillock
sugarcaneverb
romainegenerosity
oikmocha
frostretort
bunchscholarly
verdantreject
fryspanish
mutepick
kayakercrease
saladwork
musterclue
iratequilt
chimneychampion
treasurebobcat
maternallanguid
ravenimported
skiporridge
gibbonmelon
amuckrivulet
rottenguess
shirthinds
conceitedhunting
contributeproblem
sectionpad
steadysign
wadersdavit
hedgehogsquad
hazmatsoulless
bulletsnipe
gleefulremuda
shrewdtower
yearlygrown
dyethrob
cloakallude
serenetaxpayer
totembask
carekind
uppityweaver
marketdick
mortifiedpears
roledear
castfly
bottomryprojector
memorablewildfowl
palpitamessy
banannoyance
huskymore
vomershine
tenuousludicrous
builderpeak
vegetablecupcake
productiverub""".splitlines()

def random_ip():
    return ".".join([str(random.randint(1, 255)) for x in range(4)])

import argon2
import os
ph = argon2.PasswordHasher()



output = ["(1, 'admin', '{}')".format(ph.hash(os.urandom(16)))]

for user_id in range(2, 76):
    output.append("({}, '{}', '{}')".format(user_id, usernames[user_id], ph.hash(os.urandom(16))))

print("""INSERT OR REPLACE INTO users (id, username, password) VALUES {};""".format(",".join(output)))

output = []
admin_ip = "18.169.167.112 (test)"

for i in range(1, 350):
    if random.randint(0, 10) == 0:
        output.append("({}, 1, 10, '{}', 1)".format(i, admin_ip))
    else:
        payment_received = 1 if random.randint(0, 10) < 4 else 0
        output.append("({}, {}, {}, '{}', {})".format(i, random.randint(2, 76), random.randint(1, 10), random_ip(), 0))

print("""INSERT OR REPLACE INTO requests (id, user_id, service, target, payment_received) VALUES {};""".format(",".join(output)))

