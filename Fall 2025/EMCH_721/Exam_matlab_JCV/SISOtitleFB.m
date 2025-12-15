function [line1,line2] = SISOtitleFB(f,z,Kratio,f_CL,z_CL)
    % This function creates a title for SISO system plots with feedback
    % Inputs:
    %   f - frequency vector
    %   z - damping vector
    %   Kratio - Gain ratio
    %   f_CL - Closed-loop frequency vector
    %   z_CL - Closed-loop damping vector
    % Outputs:
    %   line1, line2 - Title strings on separate lines
    
    % Construct title components
    T1 = ['K ratio=' num2str(Kratio)];
    T2 = [ ' fCL=' num2str(f_CL(1),'%0.4f') 'Hz, zCL=' num2str(z_CL(1)*100) '%'];
    T3 = [ ' f=' num2str(f(1),'%0.4f') ' Hz, z= ' num2str(z(1)*100) '%'];
    
    % Combine components into two lines
    line1 = [T1 T2];
    line2 = [T3];
    
end % function ends