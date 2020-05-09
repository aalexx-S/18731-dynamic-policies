# A helper program to initialize all status value in the redis database

import redis

r = redis.Redis(host='redis', port='6379')

r.set('HomeMotion.motion', 'true')
r.set('HomeMotion.powerlevel', '1.0')

r.set('Stove1.heatlevel', '3')
r.set('Stove1.powerlevel', '1.0')

r.set('FrontWindow.openlevel', '0.5')

r.set('Aircon1.power_on', 'false')
r.set('Aircon1.temperature', '70')

r.set('Thermo1.temperature', '75.4')

r.set('Clock1.hour', '10')
r.set('Clock1.minute', '170')