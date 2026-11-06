"""Rebuild the published snapshot from preserved, source-linked research."""
import json,re,unicodedata
from pathlib import Path
root=Path(__file__).parent
research=root/'research'
data=json.loads((research/'senate_snapshot.json').read_text())
for p in data['members']:
 p['chamber']='Senate'
 p['electionSource']=data['roster']
roster=json.loads((research/'house_roster.json').read_text())
roster_members=roster.get('members',[])
def seat_key(d):
 a,b=d.split('-');return a+'-'+('AL' if b in ['AL','At-large','0','00'] else str(int(b)))
verified={seat_key(p['district']):p for p in roster_members}
house=[]
for filename in ['house_northeast.json','house_midwest.json','house_south.json','house_west.json','house_texas.json']:
 incoming=json.loads((research/filename).read_text())
 if isinstance(incoming,dict):incoming=incoming.get('members',incoming.get('profiles',[]))
 for p in incoming:
  key=seat_key(p['district'])
  if key not in verified:raise ValueError('Profile missing roster: '+p['name']+' '+key)
  r=verified[key]
  p['chamber']='House'
  p['district']=key
  p['id']=re.sub('[^a-z0-9]+','-',unicodedata.normalize('NFKD',p['name']).encode('ascii','ignore').decode().lower()).strip('-')
  p['party']={'Democrat':'D','Democratic':'D','Republican':'R'}.get(p['party'],p['party'])
  p['returning']=r.get('returning',False)
  if 'artba.org' not in r.get('electionSource',{}).get('url','artba.org'):p['electionSource']=r['electionSource']
  if 'artba.org' in p.get('electionSource',{}).get('url','artba.org'):raise ValueError('Election still unverified: '+p['name'])
  p.setdefault('campaignPriority','No dedicated data-center campaign priority verified in reviewed sources.')
  p['classificationNote']=p.get('classificationNote') or 'Explicit resource-cost safeguards support the regulation category; no blanket construction stance is inferred.'
  p['priorityLabel']={'Not established':'No position located','State legislative record':'State/local record'}.get(p.get('priorityLabel'),p.get('priorityLabel','No position located'))
  p.setdefault('priorityLabel','No position located' if not p['categories'] else 'Campaign statements')
  p.setdefault('proposals',[])
  p.setdefault('researchNote','Targeted campaign and news searches completed November 6, 2026. Coverage is not exhaustive.')
  p['sources']=[{k:v for k,v in s.items() if k not in ['ref','ref_id']} for s in p['sources']]
  house.append(p)
assert len({p['district'] for p in house})==len(house),'Duplicate House seat'
assert len(house)==len(verified),(len(house),len(verified),'Missing researched members')
data['members']+=house
data['members'].sort(key=lambda p:(p['chamber'],p['party'],p['state'],p.get('district',''),p['name']))
data['version']='2.0'
data['scope']='Called incoming voting members of the House and Senate, including returning former members; excludes sitting incumbents and nonvoting delegates.'
data['coverageNote']=f"This snapshot includes {len(house)} called House newcomers or returning former members, alongside 17 Senate profiles. It excludes serving incumbents, nonvoting delegates and unresolved races. Calls and research coverage are dated November 6; the roster can grow as counting continues."
data['housePendingNote']='The House roster is a dated research snapshot, not a final certified class. The pending list below highlights races that could add newcomers. It is not a count of all uncalled House races. Uncalled seats are not populated with presumed winners.'
data['houseRosterAudit']=roster
for p in json.loads((research/'house_pending.json').read_text())['pending']:
 data['pending'].append({'state':p.get('district',p.get('state','House race')),'description':p.get('description',p.get('note',p.get('status',p.get('reason','Unresolved race')))),'url':p.get('url',p.get('source',p.get('electionSource',{}).get('url','')))})
(root/'dist/data.js').write_text('const DATA = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n')
(root/'dist/research-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print('Prepared',len(house),'House and',len(data['members'])-len(house),'Senate profiles.')
