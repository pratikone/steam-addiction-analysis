import scipy.io as sio
from pdb import set_trace as st
import subprocess
import os
import rec_eval

import argparse

parser = argparse.ArgumentParser(description='Joint MF')
parser.add_argument('--rank', type=int , default=40)
parser.add_argument('--max_iter', type=int , default=100 )
parser.add_argument('--setting', type=int , default=1)
parser.add_argument('--dataset', type=str ,default='/home/sanket/cs6604/connectedData/dataset10000')
parser.add_argument('--model_path', type=str )
args = parser.parse_args()




rank = args.rank
maxIter = args.max_iter
d = os.path.abspath(os.path.dirname(__file__)) 
dataset = args.dataset #'/home/sloke/cs6604/connectedData/dataset10000'
setting = args.setting

if args.model_path:
	d= args.model_path
	import os
	try: 
	    os.makedirs(d)
	except OSError:
	    if not os.path.isdir(d):
	        raise

cmd = './train.sh '+dataset+' ' + str(maxIter)+' '+str(rank)+' '+d +' '+str(setting)
print cmd
# p = subprocess.Popen('rm *.mat', shell=True)
# (output, err) = p.communicate()  


# p_status = p.wait()


p = subprocess.Popen(cmd, shell=True)
(output, err) = p.communicate()  


p_status = p.wait()


T1_train = sio.loadmat(d+'/T1traindata.mat')['T1_train'][0][0][5]
T1_test = sio.loadmat(d+'/T1testdata.mat')['T1_test'][0][0][5]


T2_train = sio.loadmat(d+'/T2traindata.mat')['T2_train'][0][0][5]
T2_test = sio.loadmat(d+'/T2testdata.mat')['T2_test'][0][0][5]


T3_train = sio.loadmat(d+'/T3traindata.mat')['T3_train'][0][0][5]
T3_test = sio.loadmat(d+'/T3testdata.mat')['T3_test'][0][0][5]


T4_train = sio.loadmat(d+'/T4traindata.mat')['T4_train'][0][0][5]
T4_test = sio.loadmat(d+'/T4testdata.mat')['T4_test'][0][0][5]


T5_train = sio.loadmat(d+'/T5traindata.mat')['T5_train'][0][0][5]
T5_test = sio.loadmat(d+'/T5testdata.mat')['T5_test'][0][0][5]


#model = sio.loadmat('model.mat')['sol'][0]
model = sio.loadmat(d+'/model.mat')['sol'][0][0][0][0][0]

U = model[0]
C = model[1]
G = model[2]

vad_data = None
try:
	train_data = T1_train
	test_data = T1_test
	print 'Testing USER-GAME MATRIX'
	print 'Test Recall@20: %f' % rec_eval.recall_at_k(train_data, test_data, U, G, k=20, vad_data=vad_data)
	print 'Test Recall@50: %f' % rec_eval.recall_at_k(train_data, test_data, U, G, k=50, vad_data=vad_data)
	print 'Test NDCG@100: %f' % rec_eval.normalized_dcg_at_k(train_data, test_data, U, G, k=100, vad_data=vad_data)
	print 'Test MAP@100: %f' % rec_eval.map_at_k(train_data, test_data, U, G, k=100, vad_data=vad_data)
except:
	print 'Error'

try:
	train_data = T2_train
	test_data = T2_test

	print 'Testing USER-GROUP MATRIX'
	print 'Test Recall@20: %f' % rec_eval.recall_at_k(train_data, test_data, U, C, k=20, vad_data=vad_data)
	print 'Test Recall@50: %f' % rec_eval.recall_at_k(train_data, test_data, U, C, k=50, vad_data=vad_data)
	print 'Test NDCG@100: %f' % rec_eval.normalized_dcg_at_k(train_data, test_data, U, C, k=100, vad_data=vad_data)
	print 'Test MAP@100: %f' % rec_eval.map_at_k(train_data, test_data, U, C, k=100, vad_data=vad_data)
except:
	print 'Error'

# st()

# train_data = T5_train
# test_data = T5_test
# print 'Testing USER-USER MATRIX'
# print 'Test Recall@20: %f' % rec_eval.recall_at_k(train_data, test_data, G, Y, k=20, vad_data=vad_data)
# print 'Test Recall@50: %f' % rec_eval.recall_at_k(train_data, test_data, G, Y, k=50, vad_data=vad_data)
# print 'Test NDCG@100: %f' % rec_eval.normalized_dcg_at_k(train_data, test_data, G, Y, k=100, vad_data=vad_data)
# print 'Test MAP@100: %f' % rec_eval.map_at_k(train_data, test_data, G, Y, k=100, vad_data=vad_data)
