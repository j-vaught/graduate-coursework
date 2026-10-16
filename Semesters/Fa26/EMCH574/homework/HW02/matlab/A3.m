% A.3. Base-displacement excitation of a car suspension.
% SI calculations supply the MATLAB views and Typst figure data.
clear; clc;
addpath(fullfile(fileparts(mfilename('fullpath')), '..', '..', 'HW01', 'matlab'));
cfg = hw01_settings();
outDir = fullfile(fileparts(mfilename('fullpath')), '..', 'figures', 'src', 'solutions', 'data');
if ~exist(outDir, 'dir'), mkdir(outDir); end

inchToM = 0.0254; footToM = 0.3048; mileToM = 1609.344;
secondsPerHour = 3600;
a = 2.5 * inchToM; lambda = 105 * footToM;
fn = 0.95; zeta = [0.22, 0.10];
vmax = 125 * mileToM / secondsPerHour;
Nlambda = 2; Nf = 2000; Flim = 1.5;
gamma = 2*pi/lambda; fmax = vmax/lambda;
f = linspace(0, fmax, Nf); v = linspace(0, vmax, Nf);

% Relative spring/damper motion gives the absolute body-to-road FRF.
Habs = @(r,z) sqrt((1+(2*z.*r).^2)./((1-r.^2).^2+(2*z.*r).^2));
FRF = @(r,z) (1+2i*z.*r)./(1-r.^2+2i*z.*r);
r = f/fn; curves = cell(1,2); peaks = cell(1,2); crossings = cell(1,2);
for j=1:2
    z = zeta(j); curves{j}=Habs(r,z);
    B=4*z^2; qRoots=roots([B,2,-2]);
    qRoots=qRoots(abs(imag(qRoots))<1e-12 & real(qRoots)>0);
    qPeak=real(qRoots(1)); rp=sqrt(qPeak);
    peaks{j}=[rp*fn, Habs(rp,z), rp, rp*fn*lambda];
    assert(abs(B*qPeak^2+2*qPeak-2)<1e-12, 'Peak stationary equation residual is too large.');
    % The analytic stationary point must bound the sampled sweep maximum.
    assert(max(curves{j})<=peaks{j}(2)+1e-12 && peaks{j}(2)-max(curves{j})<1e-4);
    % Solve |H|=Flim as a quadratic in q=r^2; keep all positive roots.
    C=B-2; qLim=roots([Flim^2, Flim^2*C-B, Flim^2-1]);
    qLim=sort(real(qLim(abs(imag(qLim))<1e-12 & real(qLim)>0)));
    crossings{j}=[sqrt(qLim(:))*fn, sqrt(qLim(:))*fn*lambda];
end
vn=fn*lambda; vnMph=vn/mileToM*secondsPerHour;
vTarget=35*mileToM/secondsPerHour; lambdaNew=vTarget/fn;

% Verify the complex EOM ratio, matched response, and exact threshold events.
for j=1:2
    z=zeta(j); probes=[0,0.5,1,1.7];
    direct=(1+2i*z*probes)./(1-probes.^2+2i*z*probes);
    assert(max(abs(abs(direct)-Habs(probes,z)))<1e-12);
    assert(abs(abs(FRF(1,z))-sqrt(1+(2*z)^2)/(2*z))<1e-12);
    assert(all(abs(Habs(crossings{j}(:,1)/fn,z)-Flim)<1e-10));
end
assert(numel(f)==Nf && numel(v)==Nf);

% Exact event coordinates and labels for Typst and MATLAB datatips.
frequencyEvents=cell(1,2); speedEvents=cell(1,2); plotYmax=[4.0,6.4];
for j=1:2
    names={sprintf('Peak: %.3f Hz, %s',peaks{j}(1),format3(peaks{j}(2))), ...
        sprintf('Matched: %.3f Hz, %s',fn,format3(Habs(1,zeta(j))))};
    frequencyEvents{j}=struct('x',[peaks{j}(1),fn], ...
        'y',[peaks{j}(2),Habs(1,zeta(j))],'label',{names});
    speedEvents{j}=struct('x', ...
        [crossings{j}(1,2),peaks{j}(4),vn,crossings{j}(2,2)] ...
        *secondsPerHour/mileToM, ...
        'y',[Flim,peaks{j}(2),Habs(1,zeta(j)),Flim], ...
        'label',{{sprintf('Low limit %.1f mph',crossings{j}(1,2)*secondsPerHour/mileToM), ...
        sprintf('Peak %.1f mph, %s',peaks{j}(4)*secondsPerHour/mileToM,format3(peaks{j}(2))), ...
        sprintf('Matched %.1f mph, %s',vnMph,format3(Habs(1,zeta(j)))), ...
        sprintf('High limit %.1f mph',crossings{j}(2,2)*secondsPerHour/mileToM)}});
end

% Road profile, two wavelengths.
x=linspace(0,Nlambda*lambda,1001); ub=a*cos(gamma*x);
writeJson(fullfile(outDir,'A3-road.json'), struct('x',x,'y',ub, ...
    'xlim',[0,Nlambda*lambda],'ylim',[-1.12*a,1.12*a], ...
    'xlabel','Distance, x (m)','ylabel','Road displacement, u_b (m)'));

% Export both 2000-sample FRF sweeps and exact analytic datatip coordinates.
writeJson(fullfile(outDir,'A3-frequency.json'), struct('x',f, ...
    'yHealthy',curves{1},'yWorn',curves{2},'xlim',[0,fmax], ...
    'ylim',[0,1.12*max(curves{2})],'xlabel','Road frequency, f (Hz)', ...
    'ylabel','|U/U_b|','healthyEvents',frequencyEvents{1},'wornEvents',frequencyEvents{2}));
for j=1:2
    caseName={'healthy','worn'}; labels={'Healthy shocks, zeta = 0.22','Worn shocks, zeta = 0.10'};
    writeJson(fullfile(outDir,['A3-speed-',caseName{j},'.json']), struct( ...
        'x',v*secondsPerHour/mileToM,'y',curves{j}, ...
        'xlim',[0,vmax*secondsPerHour/mileToM], ...
        'ylim',[0,plotYmax(j)],'limit',Flim, ...
        'xlabel','Vehicle speed, v (mph)','ylabel','|U/U_b|', ...
        'curveLabel',labels{j},'variant',caseName{j},'events',speedEvents{j}));
end

% MATLAB views with exact analytic event datatips.
figRoad=figure('Name','A.3 road profile','Color','w'); ax=axes(figRoad); hold(ax,'on');
plot(ax,x,ub,'Color',cfg.colors(1,:),'LineWidth',1.3);
xlabel(ax,'Distance, x (m)'); ylabel(ax,'Road displacement, u_b (m)'); grid(ax,'on'); box(ax,'on');
figFrequency=figure('Name','A.3 frequency response','Color','w'); axf=axes(figFrequency); hold(axf,'on');
plot(axf,f,curves{1},'Color',cfg.colors(1,:),'LineWidth',1.3,'DisplayName','Healthy shocks, zeta = 0.22');
plot(axf,f,curves{2},'--','Color',cfg.colors(2,:),'LineWidth',1.3,'DisplayName','Worn shocks, zeta = 0.10');
for j=1:2, addDatatips(axf,frequencyEvents{j},cfg.colors(j,:),'Frequency (Hz)'); end
xlabel(axf,'Road frequency, f (Hz)'); ylabel(axf,'|U/U_b|'); grid(axf,'on'); box(axf,'on');
legend(axf,'Location','northwest'); xlim(axf,[0 fmax]); ylim(axf,[0 1.12*max(curves{2})]);
for j=1:2
    figSpeed=figure('Name',['A.3 ',caseName{j},' speed response'],'Color','w'); axs=axes(figSpeed); hold(axs,'on');
    plot(axs,v*secondsPerHour/mileToM,curves{j},'Color',cfg.colors(j,:),'LineWidth',1.3);
    yline(axs,Flim,':k','HandleVisibility','off');
    addDatatips(axs,speedEvents{j},cfg.colors(j,:),'Speed (mph)');
    xlabel(axs,'Vehicle speed, v (mph)'); ylabel(axs,'|U/U_b|'); grid(axs,'on'); box(axs,'on');
    xlim(axs,[0 vmax*secondsPerHour/mileToM]); ylim(axs,[0 plotYmax(j)]);
end

fprintf('a=%.12g m, lambda=%.12g m, gamma=%.12g rad/m, vmax=%.12g m/s, fmax=%.12g Hz\n',a,lambda,gamma,vmax,fmax);
fprintf('matched speed=%.12g m/s = %.12g mph; new wavelength=%.12g m\n',vn,vnMph,lambdaNew);
for j=1:2
    fprintf('zeta=%.2f: matched %.12g; peak f=%.12g Hz, M=%.12g, speed=%.12g m/s = %.12g mph\n', ...
        zeta(j),Habs(1,zeta(j)),peaks{j}(1),peaks{j}(2),peaks{j}(4), ...
        peaks{j}(4)*secondsPerHour/mileToM);
    fprintf('  limit crossings (mph):'); fprintf(' %.12g',crossings{j}(:,2)*secondsPerHour/mileToM); fprintf('\n');
end
function result=format3(value)
    decimalPlaces=max(0,2-floor(log10(abs(value))));
    result=sprintf(['%.' num2str(decimalPlaces) 'f'],value);
end
function addDatatips(ax,event,color,speedOrFrequency)
    h=scatter(ax,event.x,event.y,28,'s','MarkerEdgeColor','k', ...
        'MarkerFaceColor',color,'HandleVisibility','off');
    names=string(event.label);
    h.DataTipTemplate.DataTipRows=[dataTipTextRow('Event',names), ...
        dataTipTextRow(speedOrFrequency,event.x),dataTipTextRow('Magnitude',event.y)];
    for k=1:numel(event.x), datatip(h,event.x(k),event.y(k)); end
end
function writeJson(path,data)
    fid=fopen(path,'w'); assert(fid>=0); cleanup=onCleanup(@() fclose(fid));
    fwrite(fid,jsonencode(data),'char');
end
