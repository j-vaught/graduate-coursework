function displayUfv(U, f, v)
% displayUfv: Displays frequencies and modeshapes at various airspeeds
%
% This function prints the frequencies and corresponding modeshapes for
% each airspeed in the provided arrays.
%
% Inputs:
% U - array of airspeeds (m/s)
% f - matrix of frequencies (Hz) for each airspeed
% v - 3D array of modeshapes for each airspeed

fprintf('\n=========================================\n');
fprintf('FREQUENCIES AND MODESHAPES AT VARIOUS AIRSPEEDS\n');
fprintf('=========================================\n');

NU = length(U);
for jU = 1:NU
    fprintf('\nU = %.2f m/s\n', U(jU));
    
    % Determine number of modes
    num_modes = size(v, 2);
    
    % Print frequencies as column headers (centered in 22-char columns)
    fprintf('  ');
    for i = 1:num_modes
        fprintf('    %10.4f Hz    ', f(i, jU));
    end
    fprintf('\n  %s\n', repmat('-', 1, 22*num_modes));
    
    % Print modeshapes
    v_current = v(:, :, jU);
    for i = 1:size(v_current, 1)
        fprintf('  ');
        for j = 1:size(v_current, 2)
            val = v_current(i, j);
            if abs(imag(val)) < 1e-10
                fprintf('     %10.4f      ', real(val));
            else
                fprintf(' %7.4f %+7.4fi  ', real(val), imag(val));
            end
        end
        fprintf('\n');
    end
end

end % function displayUfv ends here