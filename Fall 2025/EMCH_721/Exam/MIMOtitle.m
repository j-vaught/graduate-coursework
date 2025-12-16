function [tFig] = MIMOtitle(fh,ft,zh,zt,CPratio,QPratio,U,f,z)
    % This function creates a title for MIMO system plots
    % Inputs:
    %   fh, ft - frequencies
    %   zh, zt - damping values
    %   CPratio, QPratio - ratios
    %   U - velocity
    %   f - frequency vector
    %   z - damping vector
    % Output:
    %   tFig - Cell array containing title lines
    
    % Construct title components
    T1 = ['U=' num2str(U) 'm/s'];
    T2a = [' f1=' num2str(f(1),'%0.1f') 'Hz'];
    T2b = [' z1=' num2str(z(1)*100,'%0.1f') '%'];
    T3a = [' f2=' num2str(f(3),'%0.1f') 'Hz'];
    T3b = [' z2=' num2str(z(3)*100,'%0.1f') '%'];
    T4 = [' xQP=' num2str(QPratio*100) '%'] ;
    T5 = [' xCP= ' num2str(CPratio*100) '%'] ;
    T6 = [' fh=' num2str(fh) 'Hz ft=' num2str(ft) 'Hz'];
    T7 = [' zh=' num2str(zh*100) '% zt=' num2str(zt*100) '%'];
    
    % Combine title components into two lines
    line1 = [T1 T2a T3a T2b T3b];
    line2 = [T4 T5 T6 T7];
    
    tFig = {line1 line2};
    
end % function ends here