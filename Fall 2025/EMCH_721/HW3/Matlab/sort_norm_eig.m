function [X_sorted_normalized,e_sorted] = sort_norm_eig(X,e)
%{
X(N,Ne) = matrix of Ne eigenvectors each of N dofs
e(Ne) = row of Ne eigenvalues
Procedure:
sort eigenvalues e in magnitude order and stores into es
reorder the eigenvector X and stores into Xs
normalize the sorted eigenvectors Xs to get Xsn
such that the largest element in each eigenvector is = 1
%}
N=size(X,1); Ne=size(X,2); % pick sizes N, Ne
e_abs=abs(e); % pick up abs values
% [~,Is]=sort(e_abs,'descend'); % sort in descending order 
[~,Is]=sort(e_abs,'ascend'); % sort in ascending order 
% Is contains the sorted indices
%% store sorted eigenvalues and eigenvectors
e_sorted=zeros(1,Ne); Xs=zeros(N,Ne);
for ne=1:Ne; e_sorted(ne)=e(Is(ne)); Xs(:,ne)=X(:,Is(ne)); end %
% display(e_sorted,'sorted eigenvalues')
% display(Xs,'sorted eigenvectors')
%% normalize eigenvectors to make +ve the largest element in each column
Xabs=abs(Xs);
[~,IX]=max(Xabs,[],1);
% allocate full N-by-Ne so we can store every sorted eigenvector
X_sorted_normalized=zeros(N); 
for j=1:Ne; 
    scale=sign(Xs(IX(j),j))*max(abs(Xs(:,j))); 
    X_sorted_normalized(:,j)=Xs(:,j)/scale; 
end
 
end % function ends her
