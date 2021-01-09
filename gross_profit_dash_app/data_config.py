import datetime

BUNDLE_LIST = [('Space_K', 'com.oneapp.max.cleaner.booster.cn'),
               ('PrivacyPowerPro_K', 'com.oneapp.max.security.pro.cn'),
               ('Optimizer_K', 'com.oneapp.max.cn'),
               ('FastClear_K', 'com.boost.clean.coin.cn'),
               ('Normandy_K', 'com.normandy.booster.cn'),
               ('500_K', 'com.honeycomb.launcher.cn'),
               ('Cookie_K', 'com.emoticon.screen.home.launcher.cn'),
               ('ColorPhone_K', 'com.colorphone.smooth.dialer.cn'),
               ('DogRaise_K', 'com.dograise.richman.cn'),
               ('Rat_K', 'com.rat.countmoney.cn'),
               ('LuckyDog_K', 'com.fortunedog.cn'),
               ('Amber_K', 'com.diamond.coin.cn'),
               ('River_K', 'com.crazystone.coin.cn'),
               ('Walk_K', 'com.walk.sports.cn'),
               ('RunFast_K', 'com.run.sports.cn'),
               ('Mars_K', 'com.cyqxx.puzzle.idiom.cn'),
               ('Athena', '1503126294'),
               ('Apollo_K', 'com.yqs.cn'),
               ('Poseidon_K', 'com.lightyear.dccj'),
               ('Ares_K', 'com.idiom.tjj.cn'),
               ('Coffee_K', 'com.drinkwater.health.coin.cn'),
               ('Emperor_K', 'com.waytoemperor.cn')]

APPS = ['Space_K', 'PrivacyPowerPro_K', 'Optimizer_K', 'FastClear_K', 'Normandy_K', '500_K', 'Cookie_K',
        'ColorPhone_K', 'DogRaise_K', 'Rat_K', 'LuckyDog_K', 'Amber_K', 'River_K',
        'Walk_K', 'RunFast_K', 'Coffee_K',
        'Mars_K', 'Athena', 'Apollo_K', 'Poseidon_K', 'Ares_K', 'Emperor_K']

TEAM_APPS = {'total': ['Space_K', 'PrivacyPowerPro_K', 'Optimizer_K', 'FastClear_K', '500_K', 'Cookie_K',
                       'ColorPhone_K', 'DogRaise_K', 'Rat_K', 'LuckyDog_K', 'Amber_K', 'River_K', 'Walk_K', 'RunFast_K',
                       'Coffee_K', 'Mars_K', 'Athena', 'Apollo_K', 'Poseidon_K', 'Ares_K', 'Emperor_K'],
             '010': ['Space_K', 'PrivacyPowerPro_K', 'Optimizer_K', 'FastClear_K', 'Amber_K', 'Walk_K',
                     'River_K', 'RunFast_K', 'Coffee_K'],
             '075': ['Mars_K', 'Athena', 'Apollo_K', 'Poseidon_K', 'Ares_K'],
             '060': ['500_K', 'Cookie_K', 'ColorPhone_K', 'DogRaise_K', 'Rat_K', 'LuckyDog_K'],
             '080': ['Normandy_K', 'Emperor_K']}

RMBperDOLLAR = 6.7

Q_TAR = {'total': 100000*RMBperDOLLAR,
         '010': 30000*RMBperDOLLAR,
         '075': 40000*RMBperDOLLAR,
         '060': 30000*RMBperDOLLAR,
         '080': 5000*RMBperDOLLAR}

YEAR_TAR = {'total': 145000*RMBperDOLLAR,
            '010': 40000*RMBperDOLLAR,
            '075': 60000*RMBperDOLLAR,
            '060': 40000*RMBperDOLLAR,
            '080': 5000*RMBperDOLLAR}

TEAMS = ['total', '075', '010', '060', '080']

Q_START = datetime.datetime(2021, 1, 1)
YEAR_START = datetime.datetime(2021, 1, 1)

