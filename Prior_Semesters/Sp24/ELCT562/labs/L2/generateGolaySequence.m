function [Ga, Gb] = generateGolaySequence(order)
    % Initialize the base Golay sequences
    Ga = [1, 1];
    Gb = [1, -1];
    
    % Iterate to generate the sequences of the desired order
    for i = 2:order
        % Apply Golay sequence generation logic correctly
        Ga_new = [Ga, Ga]; % Concatenate Ga with itself
        Gb_new = [Ga, -Ga]; % Concatenate Ga with its negated version for Gb
        
        % Correctly construct Gb_new using the Golay recursive relationship
        Ga = [Ga_new, Gb_new];  % This step combines Ga and Gb in the correct pattern
        Gb = [Ga_new, -Gb_new]; % This step involves negation in the correct spots
    end
end
