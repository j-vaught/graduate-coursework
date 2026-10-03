function analytical_checks(outputDirectory)
% J.C. Vaught. Analytical checks only, no field detection experiment.
% Run analytical_checks('data') from the project directory.
if nargin < 1
    outputDirectory = 'data';
end
if ~exist(outputDirectory, 'dir')
    mkdir(outputDirectory);
end
r = linspace(0, 3, 301)';
response = @(zeta) 1 ./ sqrt((1-r.^2).^2 + (2*zeta*r).^2);
light = response(0.12);
heavy = response(0.30);
nu = linspace(-1.5, 1.5, 301)';
J = zeros(size(nu));
use = nu > -0.78;
J(use) = 6.9 + 20*log10(sqrt((nu(use)-0.1).^2+1)+nu(use)-0.1);
G = 10.^(-J/10);
visibility = double(nu < 0);
assert(abs(light(1)-1) < 1e-12);
assert(abs(light(101)-1/(2*0.12)) < 1e-12);
assert(abs(heavy(101)-1/(2*0.30)) < 1e-12);
assert(all(isfinite([light; heavy; J; G])));
assert(all(G >= 0 & G <= 1.001));
writetable(table(r, light, heavy), fullfile(outputDirectory, 'heave_matlab.csv'));
writetable(table(nu, J, G, visibility), fullfile(outputDirectory, 'edge_matlab.csv'));
fprintf('Analytical checks passed. Edge loss at zero %.9f dB.\n', J(151));
end
