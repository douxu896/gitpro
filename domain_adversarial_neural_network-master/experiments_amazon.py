#coding:utf-8
import numpy as np
from DANN import DANN
from mSDA import compute_msda_representation
from sklearn.datasets import load_svmlight_files
from sklearn import svm


def main():
    data_folder = './data/'     # where the datasets are
    source_name = 'books'         # source domain: books, dvd, kitchen, or electronics
    target_name = 'data' # traget domain: books, dvd, kitchen, or electronics
    adversarial = True          # set to False to learn a standard NN
    msda = True

    hidden_layer_size = 50
    lambda_adapt = 0.1 if adversarial else 0.
    learning_rate = 0.001 if not msda else 0.0001
    maxiter = 100
    print("Loading data...")
    xs, ys, xt, _, xtest, ytest = load_amazon(source_name, target_name, data_folder, verbose=True)
    if msda:
        xs_path, xt_path, xtest_path = ['%s/%s.%s_%s_msda.npy' % (data_folder, source_name, target_name, E)
                                        for E in ('source', 'target', 'test')]
        # try:
        #     xs_msda = np.load(xs_path)
        #     xt_msda = np.load(xt_path)
        #     xtest_msda = np.load(xtest_path)
        #     print('mSDA representations loaded from disk')
        # except:
        print('Computing mSDA representations...')
        xs_msda, xt_msda, xtest_msda = compute_msda_representation(xs, xt, xtest)
        ds,ns=np.shape(xs_msda)
        print 'shape(xs_msda)'
        print ds,ns
        # print xs_msda
        dt,nt=np.shape(xt_msda)
        print 'shape(xt_msda)'
        print dt,nt
        # print xt_msda
        dxtest,nxtest=np.shape(xtest_msda)
        print 'shape(xtest_msda)'
        print dxtest,nxtest
        # np.save(xs_path, xs_msda)
        # np.save(xt_path, xt_msda)
        # np.save(xtest_path, xtest_msda)

        xs, xt, xtest = xs_msda, xt_msda, xtest_msda

    nb_valid = int(0.1 * len(ys))
    
    xv, yv = xs[-nb_valid:, :], ys[-nb_valid:]
    xs, ys = xs[0:-nb_valid, :], ys[0:-nb_valid]
   
    print("Fit...")
    algo = DANN(lambda_adapt=lambda_adapt, hidden_layer_size=hidden_layer_size, learning_rate=learning_rate,
                maxiter=maxiter, epsilon_init=None, seed=12342, adversarial_representation=adversarial, verbose=True)
    algo.fit(xs, ys, xt, xv, yv)

    print("Predict...")
    prediction_train = algo.predict(xs)
    prediction_valid = algo.predict(xv)
    prediction_test = algo.predict(xtest)

    
    va = count(prediction_valid)
    print  '验证集正向的预测标签比率'
    print va[0],"%.2f%%" %((float(va[0])/len(prediction_valid))*100)
    print  '验证集负向的预测标签比率'
    print va[1],"%.2f%%" %((float(va[1])/len(prediction_valid))*100)
    te = count(prediction_test)
    print  '测试集正向的预测标签比率'
    print te[0],"%.2f%%" %((float(te[0])/len(prediction_test))*100)
    print  '测试集负向的预测标签比率'
    print te[1],"%.2f%%" %((float(te[1])/len(prediction_test))*100)
    
    print('Training Risk   = %f' % np.mean(prediction_train != ys))
    print('Validation Risk = %f' % np.mean(prediction_valid != yv))
    print('Test Risk       = %f' % np.mean(prediction_test != ytest))

    print  '验证集正向和负向的预测准确率'
    print compare(yv,prediction_valid)
    print  '测试集正向和负向的预测准确率'
    print compare(ytest,prediction_test)

    print('==================================================================')

    # print('Computing PAD on DANN representation...')
    # pad_dann = compute_proxy_distance(algo.hidden_representation(xs), algo.hidden_representation(xt), verbose=True)
    # print('PAD on DANN representation = %f' % pad_dann)

    # print('==================================================================')

    # print('Computing PAD on original data...')
    # pad_original = compute_proxy_distance(xs, xt, verbose=True)
    # print('PAD on original data = %f' % pad_original)


def load_amazon(source_name, target_name, data_folder=None, verbose=False):
    """
    Load the amazon sentiment datasets from svmlight format files
    inputs:
        source_name : name of the source dataset
        target_name : name of the target dataset
        data_folder : path to the folder containing the files
    outputs:
        xs : training source data matrix
        ys : training source label vector
        xt : training target data matrix
        yt : training target label vector
        xtest : testing target data matrix
        ytest : testing target label vector
    """

    if data_folder is None:
        data_folder = 'data/'

    source_file = data_folder + source_name + '_train.svmlight'
    target_file = data_folder + target_name + '_train.svmlight'
    test_file = data_folder + target_name + '_test.svmlight'

    if verbose:
        print('source file:', source_file)
        print('target file:', target_file)
        print('test file:  ', test_file)

    xs, ys, xt, yt, xtest, ytest = load_svmlight_files([source_file, target_file, test_file])

    # Convert sparse matrices to numpy 2D array
    xs, xt, xtest = (np.array(X.todense()) for X in (xs, xt, xtest))

    # Convert {-1,1} labels to {0,1} labels
    ys, yt, ytest = (np.array((y + 1) / 2, dtype=int) for y in (ys, yt, ytest))

    return xs, ys, xt, yt, xtest, ytest


def compute_proxy_distance(source_X, target_X, verbose=False):
    """
    Compute the Proxy-A-Distance of a source/target representation
    """
    nb_source = np.shape(source_X)[0]
    nb_target = np.shape(target_X)[0]

    if verbose:
        print('PAD on', (nb_source, nb_target), 'examples')

    C_list = np.logspace(-5, 4, 10)

    half_source, half_target = int(nb_source/2), int(nb_target/2)
    train_X = np.vstack((source_X[0:half_source, :], target_X[0:half_target, :]))
    train_Y = np.hstack((np.zeros(half_source, dtype=int), np.ones(half_target, dtype=int)))

    test_X = np.vstack((source_X[half_source:, :], target_X[half_target:, :]))
    test_Y = np.hstack((np.zeros(nb_source - half_source, dtype=int), np.ones(nb_target - half_target, dtype=int)))

    best_risk = 1.0
    for C in C_list:
        clf = svm.SVC(C=C, kernel='linear', verbose=False)
        clf.fit(train_X, train_Y)

        train_risk = np.mean(clf.predict(train_X) != train_Y)
        test_risk = np.mean(clf.predict(test_X) != test_Y)

        if verbose:
            print('[ PAD C = %f ] train risk: %f  test risk: %f' % (C, train_risk, test_risk))

        if test_risk > .5:
            test_risk = 1. - test_risk

        best_risk = min(best_risk, test_risk)

    return 2 * (1. - 2 * best_risk)


def count(x):
    l = [0,0]
    for i in x:
        if i == 0:
            l[0] = l[0] + 1
        else:
            l[1] = l[1] + 1
    return l

# x representate standard
# y representate predict
def compare(x, y):
    l = [0,0,0]
    d = [0,0,0]
    for i in range(0,len(x)):
        if x[i] == 0:
            l[0] = l[0] + 1
        elif x[i] == 1:
            l[1] = l[1] + 1
        else:
            l[2] = l[2] + 1
        if x[i] == y[i] == 0:
            d[0] = d[0] + 1
        elif x[i] == y[i] == 1:
            d[1] = d[1] + 1
        else:
            d[2] = d[2] + 1
    acc = []
    
    if l[1] == 0:
        acc.append(0)
    else:
        acc.append(float(d[1])/l[1])
    if l[0] == 0:
        acc.append(0)
    else:
        acc.append(float(d[0])/l[0])
    return acc


if __name__ == '__main__':
    main()

