
from idebug import *
import idebug as dbg


def res(r, title='_None'):
    print(f"\n{'*'*60}\n Debug.res : {title}")
    print(f"\n r : {r}")
    print(f"\n type(r) : {type(r)}")
    print(f"\n r.headers :\n")
    pp.pprint(r.headers)
    print(f"\n dir(r) :\n\n {dir(r)}")
    print(f"\n r.__attrs__ :\n\n {r.__attrs__}")
    print(f"\n r.__dict__ :\n")

    dics = []
    for key, value in r.__dict__.items():
        dics.append({
            'key':key,
            'value':value,
            'type':type(value),
            'bytes':sys.getsizeof(value) })
    df = pd.DataFrame(dics)
    df = df.reindex(columns=['key','value','type','bytes'])
    dbg.dframe(df, 'response.__dict__')

def data_size_report():
    print('\n' + '='*60 + whoami(sys.modules[__name__].__file__, inspect.stack()[0][3]))
    from bson.objectid import ObjectId
    """
    data_size_report()
    """
    def PrintDataSize(x):
        pp.pprint({"len(x.encode('utf-8'))":len(x.encode('utf-8'))})
        pp.pprint({"sys.getsizeof(x)":sys.getsizeof(x)})

    print('\n' + '= '*30 + 'string')
    s = '삼성전자'
    PrintDataSize(s)


    print('\n' + '= '*30 + 'datetime')
    date_iso = '2018-09-28'
    PrintDataSize(date_iso)
    print('\n datetime.strptime(~) :')
    date = datetime.strptime(date_iso, '%Y-%m-%d')
    pp.pprint({"sys.getsizeof(date)":sys.getsizeof(date)})


    print('\n' + '= '*30 + 'ObjectId')
    obj_id = '5bb69217dc958f260ea3a1e9'
    PrintDataSize(obj_id)
    obj_id = ObjectId(obj_id)
    print('\n ObjectId(obj_id) :')
    pp.pprint({"sys.getsizeof(obj_id)":sys.getsizeof(obj_id)})

def query_attrs_표시길이제한(query, shown_cnt=10):
    """입력값 디버그시에 query 내부 리스트의 길이가 너무 길면 단축 표시한다."""
    fake_q = query.copy()
    q_keyli = fake_q.keys()
    q_keyli_len = len(q_keyli)
    i=1
    for k in q_keyli:
        print('\n'+'-'*60)
        if type(k) is list:
            if len(q_keyli(k)) > shown_cnt:
                attr_cut = q_keyli(k)[:shown_cnt]
                attr_len = len(q_keyli(k))
        i+=1
    #return {'attr_cut':attr_cut, 'attr_len':attr_len}
