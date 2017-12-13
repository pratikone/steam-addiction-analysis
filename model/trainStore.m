function exitcode = trainStore(fname,maxIter,rank,folder,setting)
%d = '/home/sanket/cs6604/connectedData/dataset10000';
d = fname;
s1 = '/game_matrix.txt';
s2 = '/group_matrix.txt';
s3 = '/friends.txt';
s5 = '/group_mapping.txt';
s6 = '/game_mapping.txt';
s4 = '/user_mapping.txt';
s7 = '/games_cooccurence.txt';
s8 = '/groups_cooccurence.txt';

d1 = dlmread(strcat(d,s4),'\t');
U = size(d1,1) ;
d2 = dlmread(strcat(d,s5),'\t');
C = size(d2,1) ;
d3 = dlmread(strcat(d,s6),'\t');
G = size(d3,1) ;


trainRatio = 0.8;
valRatio=0.0;
testRatio = 0.2;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


data = dlmread(strcat(d,s1),'\t');
[trainInd,valInd,testInd] = dividerand(data',trainRatio,valRatio,testRatio);
trainInd= trainInd';
valInd= valInd';
testInd= testInd';


T1_trainCount = size(trainInd,1);

A=zeros(1,T1_trainCount);
Values = zeros(2,T1_trainCount);
for i=1:T1_trainCount
	Values(1:2,i)=(trainInd(i,1:2)) ;
end
for i=1:T1_trainCount
	A(i)= log(trainInd(i,3)+1);
end
T1_train=struct;
T1_train.val = A;
T1_train.sub = Values' + 1;
T1_train.size = [U G];
T1_train.incomplete = true;             % The incomplete flag
T1_train = fmt(T1_train);

T1_testCount = size(testInd,1);
A=zeros(1,T1_testCount);
Values = zeros(2,T1_testCount);
for i=1:T1_testCount
	Values(1:2,i)=(testInd(i,1:2));
end
for i=1:T1_testCount
	A(i)= log(testInd(i,3)+1);
end
T1_test=struct;
T1_test.val = A;
T1_test.sub = Values' + 1;
T1_test.size = [U G];
T1_test.incomplete = true;             % The incomplete flag
T1_test = fmt(T1_test);




data = dlmread(strcat(d,s2),'\t');
[trainInd,valInd,testInd] = dividerand(data',trainRatio,valRatio,testRatio);
trainInd= trainInd';
valInd= valInd';
testInd= testInd';

T2_trainCount = size(trainInd,1);
A=ones(1,T2_trainCount);
Values = zeros(2,T2_trainCount);
for i=1:T2_trainCount
	Values(1:2,i)=(trainInd(i,1:2));
end

T2_train=struct;
T2_train.val = A;
T2_train.sub = Values' +1;
T2_train.size = [U C];
T2_train.incomplete = true;             % The incomplete flag
T2_train = fmt(T2_train);

T2_testCount = size(testInd,1);
A=ones(1,T2_testCount);
Values = zeros(2,T2_testCount);
for i=1:T2_testCount
	Values(1:2,i)=int64(testInd(i,1:2));
end


T2_test=struct;
T2_test.val = A;
T2_test.sub = Values' + 1;
T2_test.size = [U C];
T2_test.incomplete = true;             % The incomplete flag
T2_test = fmt(T2_test);


data = dlmread(strcat(d,s3),'\t');
[trainInd,valInd,testInd] = dividerand(data',trainRatio,valRatio,testRatio);
trainInd= trainInd';
valInd= valInd';
testInd= testInd';

T3_trainCount = size(trainInd,1);
A=ones(1,T3_trainCount);
Values = ones(2,T3_trainCount);
for i=1:T3_trainCount
	Values(1:2,i)=trainInd(i,1:2);
end
T3_train=struct;
T3_train.val = A;
T3_train.sub = Values' + 1;
T3_train.size = [U U];
T3_train.incomplete = true;             % The incomplete flag
T3_train = fmt(T3_train);

T3_testCount = size(testInd,1);
A=ones(1,T3_testCount);
Values = ones(2,T3_testCount);
for i=1:T3_testCount
	Values(1:2,i)=testInd(i,1:2);
end

T3_test=struct;
T3_test.val = A;
T3_test.sub = 	Values' + 1;
T3_test.size = [U U];
T3_test.incomplete = true;             % The incomplete flag
T3_test = fmt(T3_test);

% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

trainRatio = 1.0;
valRatio=0.0;
testRatio = 0.0;


data = dlmread(strcat(d,s8),'\t');
[trainInd,valInd,testInd] = dividerand(data',trainRatio,valRatio,testRatio);
trainInd= trainInd';
valInd= valInd';
testInd= testInd';

T4_trainCount = size(trainInd,1);

for i=1:T4_trainCount
	A(i)= log(trainInd(i,3)+1);
end

A=ones(1,T4_trainCount);
Values = ones(2,T4_trainCount);
for i=1:T4_trainCount
	Values(1:2,i)=trainInd(i,1:2);
end
T4_train=struct;
T4_train.val = A;
T4_train.sub = Values' + 1;
T4_train.size = [C C];
T4_train.incomplete = true;             % The incomplete flag
T4_train = fmt(T4_train);

T4_testCount = size(testInd,1);
A=ones(1,T4_testCount);
for i=1:T4_testCount
	A(i)= log(trainInd(i,3)+1);
end


Values = ones(2,T4_testCount);
for i=1:T4_testCount
	Values(1:2,i)=testInd(i,1:2);
end

T4_test=struct;
T4_test.val = A;
T4_test.sub = 	Values' + 1;
T4_test.size = [C C];
T4_test.incomplete = true;             % The incomplete flag
T4_test = fmt(T4_test);


data = dlmread(strcat(d,s7),'\t');
[trainInd,valInd,testInd] = dividerand(data',trainRatio,valRatio,testRatio);
trainInd= trainInd';
valInd= valInd';
testInd= testInd';

T5_trainCount = size(trainInd,1);
A=ones(1,T5_trainCount);
Values = ones(2,T5_trainCount);
for i=1:T5_trainCount
	Values(1:2,i)=trainInd(i,1:2);
end
for i=1:T5_trainCount
	A(i)= log(trainInd(i,3)+1);
end

T5_train=struct;
T5_train.val = A;
T5_train.sub = Values' + 1;
T5_train.size = [G G];
T5_train.incomplete = true;             % The incomplete flag
T5_train = fmt(T5_train);


T5_testCount = size(testInd,1);
for i=1:T5_testCount
	A(i)= log(trainInd(i,3)+1);
end

A=ones(1,T5_testCount);
Values = ones(2,T5_testCount);
for i=1:T5_testCount
	Values(1:2,i)=testInd(i,1:2);
end

T5_test=struct;
T5_test.val = A;
T5_test.sub = 	Values' + 1;
T5_test.size = [G G];
T5_test.incomplete = true;             % The incomplete flag
T5_test = fmt(T5_test);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%





format long g;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

options=struct;
options.Display = 1;
%options.CGMaxIter = 500;
options.MaxIter = maxIter;


% Co-embedding only Games + Games
if setting==1
	% Define model variables.
	model = struct;
	model.variables.u = randn(U,rank);
	model.variables.g = randn(G,rank);
	model.variables.y = randn(G,rank);
	model.factors.U = {'u'  };
	model.factors.G = { 'g'   };
	model.factors.Y =  {'y'  };
	model.factorizations.yfac.data = fmt(T1_train);
	model.factorizations.yfac.cpd  = {'U', 'G'};
	model.factorizations.comatrix2.data= fmt(T5_train);
	model.factorizations.comatrix2.cpd  = {'G', 'Y'};
	model.factorizations.regU.regL2  = {'U'};
	model.factorizations.regG.regL2  = {'G'};
	model.factorizations.regC.regL2   = {'Y'};
% Co-embedding only Community + Community
elseif setting==2
	% Define model variables.
	model = struct;
	model.variables.u = randn(U,rank);
	model.variables.c = randn(C,rank);
	model.variables.y1 = randn(C,rank);
	model.factors.U = {'u'  };
	model.factors.C = { 'c'  };
	model.factors.Y1 =  {'y1'  };
	model.factorizations.xfac.data = fmt(T2_train);
	model.factorizations.xfac.cpd  = {'U', 'C'};
	model.factorizations.comatrix2.data= fmt(T4_train);
	model.factorizations.comatrix2.cpd  = {'C', 'Y1'};
	model.factorizations.regU.regL2  = {'U'};
	model.factorizations.regC.regL2   = {'C'};
	model.factorizations.regC.regL2   = {'Y1'};
% Co-embedding Games and Community Joint factorizations
elseif setting==3
	model = struct;
	model.variables.u = randn(U,rank);
	model.variables.c = randn(C,rank);
	model.variables.g = randn(G,rank);
	model.variables.y1 = randn(C,rank);
	model.variables.y2 = randn(G,rank);
	model.factors.U = {'u'  };
	model.factors.C = { 'c'  };
	model.factors.G = { 'g'   };
	model.factors.Y1 =  {'y1'  };
	model.factors.Y2 =  {'y2'  };
	model.factorizations.xfac.data = fmt(T2_train);
	model.factorizations.xfac.cpd  = {'U', 'C'};
	model.factorizations.yfac.data = fmt(T1_train);
	model.factorizations.yfac.cpd  = {'U', 'G'};
	model.factorizations.comatrix2.data= fmt(T4_train);
	model.factorizations.comatrix2.cpd  = {'C', 'Y1'};
	model.factorizations.comatrix3.data= fmt(T5_train);
	model.factorizations.comatrix3.cpd  = {'G', 'Y2'};
	model.factorizations.regU.regL2  = {'U'};
	model.factorizations.regC.regL2   = {'C'};
	model.factorizations.regG.regL2  = {'G'};
	model.factorizations.regC.regL2   = {'Y1'};
	model.factorizations.regG.regL2  = {'Y2'};
% Co-embedding Games  Joint factorizations
elseif setting==4
	model = struct;
	model.variables.u = randn(U,rank);
	model.variables.c = randn(C,rank);
	model.variables.g = randn(G,rank);
	model.variables.y2 = randn(G,rank);
	model.factors.U = {'u'  };
	model.factors.C = { 'c'  };
	model.factors.G = { 'g'   };
	model.factors.Y2 =  {'y2'  };
	model.factorizations.xfac.data = fmt(T2_train);
	model.factorizations.xfac.cpd  = {'U', 'C'};
	model.factorizations.yfac.data = fmt(T1_train);
	model.factorizations.yfac.cpd  = {'U', 'G'};
	model.factorizations.comatrix3.data= fmt(T5_train);
	model.factorizations.comatrix3.cpd  = {'G', 'Y2'};
	model.factorizations.regU.regL2  = {'U'};
	model.factorizations.regC.regL2   = {'C'};
	model.factorizations.regG.regL2  = {'G'};
	model.factorizations.regG.regL2  = {'Y2'};
% Co-embedding Community Joint factorizations
elseif setting==5
	model = struct;
	model.variables.u = randn(U,rank);
	model.variables.c = randn(C,rank);
	model.variables.g = randn(G,rank);
	model.variables.y1 = randn(C,rank);
	model.factors.U = {'u'  };
	model.factors.C = { 'c'  };
	model.factors.G = { 'g'   };
	model.factors.Y1 =  {'y1'  };
	model.factorizations.xfac.data = fmt(T2_train);
	model.factorizations.xfac.cpd  = {'U', 'C'};
	model.factorizations.yfac.data = fmt(T1_train);
	model.factorizations.yfac.cpd  = {'U', 'G'};
	model.factorizations.comatrix2.data= fmt(T4_train);
	model.factorizations.comatrix2.cpd  = {'C', 'Y1'};
	model.factorizations.regU.regL2  = {'U'};
	model.factorizations.regC.regL2   = {'C'};
	model.factorizations.regG.regL2  = {'G'};
	model.factorizations.regC.regL2   = {'Y1'};
% Joint factorizations
elseif setting==6
	model = struct;
	model.variables.u = randn(U,rank);
	model.variables.c = randn(C,rank);
	model.variables.g = randn(G,rank);
	model.factors.U = {'u'  };
	model.factors.C = { 'c'  };
	model.factors.G = { 'g'   };
	model.factorizations.xfac.data = fmt(T2_train);
	model.factorizations.xfac.cpd  = {'U', 'C'};
	model.factorizations.yfac.data = fmt(T1_train);
	model.factorizations.yfac.cpd  = {'U', 'G'};
	model.factorizations.regU.regL2  = {'U'};
	model.factorizations.regC.regL2   = {'C'};
	model.factorizations.regG.regL2  = {'G'};
elseif setting==7
	model = struct;
	model.variables.u = randn(U,rank);
	model.variables.c = randn(C,rank);
	model.factors.U = {'u'  };
	model.factors.C = { 'c'  }
	model.factorizations.xfac.data = fmt(T2_train);
	model.factorizations.xfac.cpd  = {'U', 'C'};
	model.factorizations.regU.regL2  = {'U'};
	model.factorizations.regC.regL2   = {'C'};
elseif setting==8
	model = struct;
	model.variables.u = randn(U,rank);
	model.variables.g = randn(G,rank);
	model.factors.U = {'u'  };
	model.factors.G = { 'g'   };
	model.factorizations.yfac.data = fmt(T1_train);
	model.factorizations.yfac.cpd  = {'U', 'G'};
	model.factorizations.regU.regL2  = {'U'};
	model.factorizations.regG.regL2  = {'G'};
end

sdf_check(model);
[sol,output] = sdf_minf(model,options);
save(strcat(folder,'/model'),'sol');

% Save Train and Test Splits
save(strcat(folder,'/T1traindata'),'T1_train');
save(strcat(folder,'/T1testdata'),'T1_test');

save(strcat(folder,'/T2traindata'),'T2_train');
save(strcat(folder,'/T2testdata'),'T2_test');

save(strcat(folder,'/T3traindata'),'T3_train');
save(strcat(folder,'/T3testdata'),'T3_test');

save(strcat(folder,'/T4traindata'),'T4_train');
save(strcat(folder,'/T4testdata'),'T4_test');

save(strcat(folder,'/T5traindata'),'T5_train');
save(strcat(folder,'/T5testdata'),'T5_test');


end
