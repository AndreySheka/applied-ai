import numpy as np
def run_open_tests(namespace=None):
    n=globals() if namespace is None else namespace
    cm,ep,rm,ct,mb=[n[name] for name in ('cosine_matrix','ensemble_prototypes','retrieval_metrics','choose_threshold','match_boxes')]
    def raises(f):
        try:f()
        except ValueError:return
        raise AssertionError('ValueError expected')
    np.testing.assert_allclose(cm([[3,0],[0,0]],[[0,2],[-5,0]]),[[0,-1],[0,0]],atol=1e-10)
    np.testing.assert_allclose(cm([[1e-200,0]],[[1e200,0]]),[[1.]])
    np.testing.assert_allclose(ep([[1e200,0],[0,1e-200]],[0,0])[1],[[2**-.5,2**-.5]])
    assert cm(np.zeros((0,2)),np.zeros((3,2))).shape==(0,3)
    raises(lambda:cm([[1,np.nan]],[[1,1]]));raises(lambda:cm([[1]],[[1,1]]))
    c,p=ep([[10,0],[0,1],[-1,0]],[0,0,1])
    assert c.tolist()==[0,1];np.testing.assert_allclose(p,[[2**-.5,2**-.5],[-1,0]])
    np.testing.assert_allclose(ep([[1,0],[-1,0]],[0,0])[1],[[0,0]])
    raises(lambda:ep([[1,0]],[]))
    r=rm([[3,2,1]],[[1,0,1]],2)
    np.testing.assert_allclose([r['precision'],r['recall'],r['hit'],r['mrr'],r['map']],[.5,.5,1,1,5/6])
    assert rm([[1,1,0]],[[0,1,0]],1)['mrr']==.5 # stable tie: image index 0 first
    assert all(v==0 for v in rm([[2,1]],[[0,0]],1).values())
    raises(lambda:rm([[1]],[[1]],0))
    assert ct([.1,.2,.01,.02],[1,1,0,0],[0,.05,.09,.3])==(.09,1.)
    raises(lambda:ct([.2],[1],[0,.1]))
    b=[[0,0,10,10],[0,0,10,10],[20,20,30,30]]
    pairs,tp,fp,fn=mb(b,[.9,.8,.7],[[0,0,10,10]],.5)
    assert pairs.tolist()==[[0,0]] and (tp,fp,fn)==(1,2,0)
    assert mb([],[],[[0,0,2,2]])[1:]==(0,0,1)
    assert mb([[0,0,2,2]],[.5],[])[1:]==(0,1,0)
    assert mb([[0,0,2,2]],[.5],[[0,0,2,2]],1)[1:]==(1,0,0)
    raises(lambda:mb([[2,0,1,2]],[.5],[]))
    print('Открытые проверки: 20 групп примеров пройдены.')
