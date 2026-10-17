% A.3. Car motion under road displacement excitation.
clear; clc; close all;
a = 2.5*0.0254; L = 105*0.3048;  % road amplitude and wavelength, m
fn = 0.95; z = [0.22 0.10];      % natural frequency, Hz; damping ratios
vm = 125*0.44704; N = 2000;      % maximum speed, m/s; sample count
b = 1.5;                        % amplification limit
C = [0 95 115; 213 94 0]/255;     % HW01 teal and orange
disp(table(a,L,fn,z(1),z(2),vm,N,b, ...
    'VariableNames',{'a','L','fn','z1','z2','vm','N','b'}));

% A.3.2--4. Road profile and excitation frequency.
g = 2*pi/L; fm = vm/L;
x = linspace(0,2*L,1001);
f = linspace(0,fm,N); v = f*L;
r = f/fn;
h = @(r,z) sqrt((1+(2*z*r).^2)./((1-r.^2).^2+(2*z*r).^2));
fprintf('Wavenumber = %.6g rad/m; maximum frequency = %.6g Hz\n',g,fm);
figure;
plot(x,a*cos(g*x),'Color',C(1,:),'LineWidth',1.3);
xlabel('Distance, x (m)'); ylabel('Road displacement, u_b (m)');
grid on; box on;

% A.3.5--10. Healthy and worn shocks.
vn = fn*L; Ln = 35*0.44704/fn;
fprintf('Matched speed = %.6g m/s = %.6g mph\n',vn,vn/0.44704);
fprintf('Wavelength for 35 mph matched speed = %.6g m\n',Ln);
figure; hold on;
plot(f,h(r,z(1)),'Color',C(1,:),'LineWidth',1.3);
plot(f,h(r,z(2)),'--','Color',C(2,:),'LineWidth',1.3);
xlabel('Road frequency, f (Hz)'); ylabel('|U/U_b|');
legend('Healthy shocks','Worn shocks'); grid on; box on;

for j = 1:2
    H = h(r,z(j));
    rp = sqrt(2/(1+sqrt(1+8*z(j)^2)));
    fp = rp*fn; vp = fp*L; hp = h(rp,z(j)); hn = h(1,z(j));
    q = roots([b^2, b^2*(4*z(j)^2-2)-4*z(j)^2, b^2-1]);
    vl = sort(sqrt(q)*fn*L);
    fprintf('\nzeta = %.2f\n',z(j));
    fprintf('Matched magnitude = %.6g\n',hn);
    fprintf('Peak = %.6g at %.6g Hz and %.6g mph\n',hp,fp,vp/0.44704);
    fprintf('Limit speeds = %.6g and %.6g mph\n', ...
        vl(1)/0.44704,vl(2)/0.44704);
    figure;
    plot(v/0.44704,H,'Color',C(j,:),'LineWidth',1.3);
    yline(b,':k');
    xlabel('Vehicle speed, v (mph)'); ylabel('|U/U_b|');
    legend(sprintf('zeta = %.2f',z(j)),'Limit');
    grid on; box on;
end
