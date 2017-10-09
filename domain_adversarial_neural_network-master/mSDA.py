import numpy as np


def compute_msda_representation(x_source, x_target, x_test):
    # length of x_source
    nb_souce = np.shape(x_source)[0]
    nb_target = np.shape(x_target)[0]
    # print "x_source: "
    # print x_source
    # print "x_target: "
    # print x_target
    # merge x_xource and x_target in chui zhi fang xiang
    x_train = np.vstack((x_source, x_target))
    # print "x_train: "
    # print x_train
    # x.train.T means zhuan zhi new_x_train means stacked hidden representations W:list of mapping 
    new_x_train, W = msda_fit(x_train.T,0.3,5,True)
    # print('w',W)
    # print('new_x_train ',new_x_train)   
    mew_x_source = new_x_train[:,:nb_souce].T
    new_x_target = new_x_train[:,nb_target:].T
    # print('new_x_source ',mew_x_source)
    # print 'new_x_target '
    # print new_x_target
    # print 'new_x_target2'
    # new_x_test:stacked hidden representations of X.
    new_x_test = msda_forward(x_test.T, W).T
    # print 'x-test'
    # print x_test
    # print 'new_x-test'
    # print new_x_test
    # print mew_x_source, new_x_target, new_x_test
    return mew_x_source, new_x_target, new_x_test


def mda_fit(X, noise=0.5, eta=1e-5):
    """
    inputs: 
        X : d x n input (Transpose of the usual data-matrix)
        noise: corruption level
        eta: regularization 
    
    outputs:
        hx: d x n hidden representation
        W: d x (d+1) mapping
    """
    d, n = np.shape(X)
   
    # adding bias
    Xb = np.vstack((X, np.ones(n)))
   
    # scatter matrix S
    S = np.dot(Xb, Xb.T)
    # corruption vector
    q = np.ones((d+1, 1)) * (1.-noise)
    q[-1] = 1
    
    # Q: (d+1)x(d+1)
    Q = S*np.dot(q,q.T)
    Q[np.diag_indices_from(Q)] = q.T[0] * np.diag(S)

    #P: dx(d+1)
    P = S[0:-1,:] * q.T 
    
    # final W = P*Q^-1, dx(d+1)
    reg = eta * np.eye(d+1)
    reg[-1,-1] = 0
    W = np.linalg.solve(Q.T + reg, P.T).T
    
    hx = np.tanh(np.dot(W, Xb))
    
    return hx, W

   
def msda_fit(X, noise=0.1, nb_layers=5, verbose=False):
    """
    inputs:
        X : d x n input Transpose of the usual data-matrix)
        noise: corruption level
        nb_layers: number of layers to stack

    outputs:
        allhx: (1+nb_layers)*d x n stacked hidden representations
        W_list: list of mapping (of size nb_layers)
    """
    eta = 1e-05
    allhx = X.copy()
    prevhx = X
    W_list = []
    
    for i in range(nb_layers):
        if verbose: print('layer =', i)
        newhx, W = mda_fit(prevhx, noise, eta)
        W_list.append(W)
        allhx = np.vstack((allhx, newhx))
        prevhx = newhx

    return allhx, W_list


def msda_forward(X, W_list):
    """
    inputs: 
        X : d x n input (Transpose of the usual data-matrix)
        noise: corruption level
        W_list: list of mapping (of size nb_layers) learned by mSDA.
    
    outputs:
        allhx: (1+nb_layers)*d x n stacked hidden representations of X.
        
    """
    _, n = np.shape(X)   
    hx = X    
    
    allhx = X.copy()
    for W in W_list:
        hxb = np.vstack(( hx, np.ones(n)) )
        hx = np.tanh( np.dot(W, hxb) )        
        allhx = np.vstack( (allhx, hx) )
        
    return allhx    
    
