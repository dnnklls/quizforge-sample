import json,re,difflib,random
from pathlib import Path
random.seed(42)
old_path=Path('data/questions.json')
in_path=Path('incoming_zip/jcl_jc99_cbt_question_bank.json')
qs=json.loads(old_path.read_text())
incoming=json.loads(in_path.read_text())

def norm(s): return re.sub(r'[^a-z0-9]+',' ',str(s).lower()).strip()
def canon_answer(s):
    n=norm(s)
    n=re.sub(r'^(the|a|an) ', '', n)
    n=n.replace('gm','g')
    return n

BAD_ANSWERS={
 'non alcoholic beverages','non-alcoholic beverages','ethnic meals','meal service','alcoholic beverages','alcoholic beverages wines',
 'main course','breakfast service','wine service','jcl service','equipment','food preparation'
}
def quality_ok(q,a):
    nq,na=norm(q),norm(a)
    if not nq or not na: return False
    if na in BAD_ANSWERS: return False
    if len(nq)<8 or len(na)<1: return False
    if len(nq)>220 or len(na)>160: return False
    # Skip obvious sentence fragments caused by PDF line wrapping.
    if na.startswith(('and ','or ','requests ','dioxide release ','sauces and ','spoon base ')): return False
    # Skip rows where true/false got glued into a partial answer instead of being the answer.
    if na not in ('true','false') and (na.endswith(' true') or na.endswith(' false')): return False
    # Skip rows where the question itself swallowed the answer then got a heading as answer.
    if (nq.endswith(' true') or nq.endswith(' false')) and na in BAD_ANSWERS: return False
    return True
def title_q(s):
    s=' '.join(str(s).replace('pax','passenger').replace('Pax','Passenger').split())
    s=s.strip(' .')
    replacements=[('hanakoreki','Hanakoireki'),('hanakoireki','Hanakoireki'),('jcl','JCL'),('jc99','JC99'),('sia','SIA'),('btc','BTC'),('spml','SPML'),('bmw','BMW'),('methode champenoise','méthode champenoise')]
    for old,new in replacements:
        s=re.sub(r'\b'+re.escape(old)+r'\b',new,s,flags=re.I)
    if s and s[0].islower(): s=s[0].upper()+s[1:]
    if not s.endswith('?') and not s.endswith(':'):
        s+='?'
    return s

def cat(q,a):
    s=(q+' '+a).lower()
    if any(x in s for x in ['wine','champagne','port','sake','vermouth','tannin','vintage','appellation','grape','cafe','espresso','coffee','lassi','beverage','drink','glass','juice','brandy','alcohol','tea']): return 'Beverages'
    if any(x in s for x in ['satay','bread','garlic','cheese','dessert','meal','breakfast','cereal','hanako','indian','passenger','pax','service','tray','main course','supper','brunch','lunch','dinner','fruit','salad','hors']): return 'Meal Service'
    if any(x in s for x in ['heat','oven','cooking','dry heat','microwave','searing','broiling','blanched','papillote','baking','boiling','steam']): return 'Food Preparation'
    if any(x in s for x in ['seat','headset','linen','flight','slippers','tube socks','call button','weber']): return 'Cabin Procedures'
    if any(x in s for x in ['plate','bowl','sauce boat','coaster','towel','cutlery','linen','dish']): return 'Equipment'
    return 'JCL CBT'

def diff(a):
    a=str(a)
    if norm(a) in ('true','false'): return 'Easy'
    if len(a)>85 or ',' in a or ';' in a: return 'Hard'
    return 'Medium'
curated={
 'glass':['Water glass','Wine glass','Champagne flute','Brandy goblet','Whiskey tumbler','Shot glass','Multi-purpose glass'],
 'time':['4 minutes','4–6 minutes','10 minutes','15 minutes','20 minutes','24 hours before departure','48 hours before departure'],
 'number':['1','2','3','4','5','6','7'],
 'wine':['Vintage','Fortified wine','Aromatized wine','Sparkling wine','Red wines','White wines','Port wine','Champagne'],
 'country':['Portugal','France','Italy','United States','Australia','Chile'],
 'position':["4 o'clock position","6 o'clock position","9 o'clock position","12 o'clock position",'Top right of the tray','Top left of the tray','Bottom right of the tray','Bottom left of the tray'],
 'service':['Upon push-back','After take-off','Before landing','On request basis','Together with the main course on a side plate','During dessert service'],
 'food':['Cornmeal','Mascarpone','Custard made with cream','Fruit stew','Stock, butter and flour','Onions and cucumber','Saucer and tablespoon'],
}
def ans_kind(q,a):
    s=(q+' '+a).lower()
    if norm(a) in ('true','false'): return 'tf'
    if 'glass' in s or 'goblet' in s or 'flute' in s or 'tumbler' in s: return 'glass'
    if re.search(r'\b\d+\s*(minutes?|mins?|hours?|hrs?)\b', s) or 'how long' in s or 'heated' in s: return 'time'
    if re.fullmatch(r'\d+', norm(a)) or 'how many' in s: return 'number'
    if any(x in s for x in ['wine','champagne','grape','vermouth','vintage','tannin','port']): return 'wine'
    if 'country' in s or 'old world' in s or ' from ' in s: return 'country'
    if 'position' in s or 'tray' in s: return 'position'
    if any(x in s for x in ['when should','basis','offered','served','service']): return 'service'
    if any(x in s for x in ['panna','polenta','compote','sauce','cheese','bread','satay','cereal','dessert','food']): return 'food'
    return None
corpus={}
for q in qs:
    corpus.setdefault(q['category'],[]).append(q['options'][q['answer']])
for x in incoming:
    corpus.setdefault(cat(x['question'],x['answer']),[]).append(str(x['answer']))
for c in corpus:
    seen=[]
    for a in corpus[c]:
        if a and a not in seen and norm(a) not in ('true','false') and len(a)<95: seen.append(a)
    corpus[c]=seen

def make_options(q,a,c):
    a=str(a).strip(); na=norm(a)
    if na in ('true','false'):
        opts=['True','False']; return opts, 0 if na=='true' else 1
    kind=ans_kind(q,a); pool=[]
    if kind and kind in curated: pool+=curated[kind]
    pool+=corpus.get(c,[])
    opts=[a]
    for x in pool:
        if norm(x)!=na and x not in opts and len(opts)<4:
            opts.append(x)
    for vals in curated.values():
        for x in vals:
            if norm(x)!=na and x not in opts and len(opts)<4:
                opts.append(x)
    opts=opts[:4]
    random.shuffle(opts)
    return opts, opts.index(a)
old_pairs=[(norm(q['question']), canon_answer(q['options'][q['answer']]), q['id']) for q in qs]
added=[]; skipped=[]
next_num=max(int(q['id'].split('-')[1]) for q in qs if q['id'].startswith('jcl-'))+1
for x in incoming:
    rawq=str(x.get('question','')).strip(); rawa=str(x.get('answer','')).strip()
    if not rawq or not rawa: continue
    if not quality_ok(rawq, rawa): continue
    nq,na=norm(rawq),canon_answer(rawa)
    best=0
    best_q=0
    same_answer_seen=False
    for oq,oa,oid in old_pairs:
        qr=difflib.SequenceMatcher(None,nq,oq).ratio()
        best_q=max(best_q,qr)
        if oa==na:
            same_answer_seen=True
            best=max(best,qr)
    # Skip same/near-same prompts even when answer wording differs slightly.
    # For distinctive non-boolean answers, the same answer usually means the same fact.
    if best_q>.68 or (na not in ('true','false') and len(na)>8 and same_answer_seen and best>.25) or best>.78:
        skipped.append((rawq,rawa,max(best,best_q))); continue
    c=cat(rawq,rawa); opts,idx=make_options(rawq,rawa,c)
    item={'id':f'jcl-{next_num:03d}','category':c,'difficulty':diff(rawa),'question':title_q(rawq),'options':opts,'answer':idx,'explanation':'Correct answer: '+opts[idx]+'.','source':'Uploaded ZIP: '+str(x.get('source','question_bank'))}
    qs.append(item); added.append(item); old_pairs.append((norm(item['question']),canon_answer(opts[idx]),item['id'])); next_num+=1
for q in qs:
    assert len(q['options']) in (2,4), (q['id'],q['options'])
    assert 0 <= q['answer'] < len(q['options']), q['id']
    assert len(q['options'])==len(set(q['options'])), q['id']
old_path.write_text(json.dumps(qs,ensure_ascii=False,indent=2)+'\n')
Path('data/questions.js').write_text('window.QUESTION_POOL = '+json.dumps(qs,ensure_ascii=False,indent=2)+';\n')
Path('data/imported_jcl_jc99_question_bank.json').write_text(json.dumps(incoming,ensure_ascii=False,indent=2)+'\n')
print('incoming', len(incoming), 'added', len(added), 'skipped_dupes', len(skipped), 'total', len(qs))
print(json.dumps(added[:2],ensure_ascii=False,indent=2))
